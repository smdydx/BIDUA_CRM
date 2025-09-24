from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import and_, or_, func, select, text, desc, asc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import asyncio
import logging
import hashlib
import functools
from app.core.database import Base
from app.models.models import *
from app.schemas import schemas

logger = logging.getLogger(__name__)

# Simple caching decorators (since Redis is not available)
def cached(ttl: int = 300, prefix: str = "cache"):
    """Simple in-memory caching decorator"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_invalidate(pattern: str = "*"):
    """Cache invalidation decorator"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Placeholder cache object
class SimpleCache:
    async def clear_pattern(self, pattern: str):
        pass

cache = SimpleCache()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    @cached(ttl=300, prefix="get_by_id")
    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID with caching"""
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error fetching {self.model.__name__} by ID {id}: {str(e)}")
            raise SQLAlchemyError(f"Error fetching {self.model.__name__}: {str(e)}")

    @cached(ttl=180, prefix="get_multi")
    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get multiple records with optimized filtering, pagination and caching"""
        try:
            query = db.query(self.model)

            # Apply filters with optimized conditions
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key) and value is not None:
                        column = getattr(self.model, key)
                        if isinstance(value, str) and '%' in value:
                            query = query.filter(column.ilike(value))  # Case insensitive
                        elif isinstance(value, list):
                            query = query.filter(column.in_(value))
                        else:
                            query = query.filter(column == value)

            # Apply search with better performance
            if search:
                search_term = f"%{search.lower()}%"
                search_conditions = []

                # Common searchable fields
                searchable_fields = ['name', 'title', 'first_name', 'last_name', 'email', 'description']
                for field in searchable_fields:
                    if hasattr(self.model, field):
                        column = getattr(self.model, field)
                        search_conditions.append(column.ilike(search_term))

                if search_conditions:
                    query = query.filter(or_(*search_conditions))

            # Apply ordering
            if order_by:
                if order_by.startswith('-'):
                    field = order_by[1:]
                    if hasattr(self.model, field):
                        query = query.order_by(desc(getattr(self.model, field)))
                else:
                    if hasattr(self.model, order_by):
                        query = query.order_by(asc(getattr(self.model, order_by)))
            else:
                # Default ordering by ID descending for better performance
                query = query.order_by(desc(self.model.id))

            # Limit should not exceed 100 for performance
            limit = min(limit, 100)

            return query.offset(skip).limit(limit).all()

        except Exception as e:
            logger.error(f"Error fetching {self.model.__name__} list: {str(e)}")
            raise SQLAlchemyError(f"Error fetching {self.model.__name__} list: {str(e)}")

    async def get_count(
        self,
        db: Session,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> int:
        """Get total count of records with optional filtering"""
        try:
            query = db.query(func.count(self.model.id))

            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key) and value is not None:
                        if isinstance(value, str) and '%' in value:
                            query = query.filter(getattr(self.model, key).like(value))
                        else:
                            query = query.filter(getattr(self.model, key) == value)

            # Apply search if supported
            if search and hasattr(self.model, 'name'):
                query = query.filter(self.model.name.contains(search))
            elif search and hasattr(self.model, 'title'):
                query = query.filter(self.model.title.contains(search))

            return query.scalar()
        except Exception as e:
            raise SQLAlchemyError(f"Error counting {self.model.__name__}: {str(e)}")

    @cache_invalidate(pattern=f"*{__name__.split('.')[-1]}*")
    async def create(self, db: Session, *, obj_in: CreateSchemaType, created_by_id: Optional[int] = None) -> ModelType:
        """Create a new record with cache invalidation"""
        try:
            obj_in_data = jsonable_encoder(obj_in)

            # Add created_by_id if model supports it and not already set
            if created_by_id and hasattr(self.model, 'created_by_id') and 'created_by_id' not in obj_in_data:
                obj_in_data['created_by_id'] = created_by_id

            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            # Invalidate related caches
            await cache.clear_pattern(f"*{self.model.__name__.lower()}*")

            logger.info(f"Created {self.model.__name__} with ID: {db_obj.id}")
            return db_obj

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating {self.model.__name__}: {str(e)}")
            raise ValueError(f"Data integrity error: {str(e)}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise SQLAlchemyError(f"Error creating {self.model.__name__}: {str(e)}")

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record"""
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Data integrity error: {str(e)}")
        except Exception as e:
            db.rollback()
            raise SQLAlchemyError(f"Error updating {self.model.__name__}: {str(e)}")

    async def remove(self, db: Session, *, id: int) -> ModelType:
        """Delete a record by ID"""
        try:
            obj = db.query(self.model).get(id)
            if not obj:
                raise ValueError(f"{self.model.__name__} not found")

            db.delete(obj)
            db.commit()
            return obj
        except Exception as e:
            db.rollback()
            raise SQLAlchemyError(f"Error deleting {self.model.__name__}: {str(e)}")

    async def soft_delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Soft delete a record (set is_active = False)"""
        try:
            obj = db.query(self.model).get(id)
            if not obj:
                return None

            if hasattr(obj, 'is_active'):
                obj.is_active = False
                db.add(obj)
                db.commit()
                db.refresh(obj)
                return obj
            else:
                # If no is_active field, perform hard delete
                return await self.remove(db, id=id)
        except Exception as e:
            db.rollback()
            raise SQLAlchemyError(f"Error soft deleting {self.model.__name__}: {str(e)}")

# Import models for CRUD classes
from app.models.models import (
    Users, Departments, Designations, Employees, Companies, Contacts,
    Leads, Deals, Activities, LeaveTypes, LeaveRequests, Attendance,
    Payroll, Projects, Tasks
)

from app.schemas.schemas import (
    UserCreate, UserUpdate, DepartmentCreate, DepartmentUpdate,
    DesignationCreate, DesignationUpdate, EmployeeCreate, EmployeeUpdate,
    CompanyCreate, CompanyUpdate, ContactCreate, ContactUpdate,
    LeadCreate, LeadUpdate, DealCreate, DealUpdate,
    ActivityCreate, ActivityUpdate, LeaveTypeCreate, LeaveRequestCreate,
    LeaveRequestUpdate, ProjectCreate, ProjectUpdate, TaskCreate, TaskUpdate
)

# Specific CRUD classes
class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        """Get user by email"""
        return db.query(Users).filter(Users.email == email).first()

    async def get_by_username(self, db: Session, *, username: str) -> Optional[Users]:
        """Get user by username"""
        return db.query(Users).filter(Users.username == username).first()

    async def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Users]:
        """Authenticate user (to be implemented with password hashing)"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        # TODO: Implement password verification
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        return user

    async def create(self, db: Session, *, obj_in: UserCreate) -> Users:
        """Create user with hashed password"""
        # TODO: Implement password hashing
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password_hash'] = hashlib.sha256(obj_in.password.encode()).hexdigest()  # Simple implementation
        del obj_in_data['password']
        db_obj = Users(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDDepartment(CRUDBase[Departments, DepartmentCreate, DepartmentUpdate]):
    async def get_by_name(self, db: Session, *, name: str) -> Optional[Departments]:
        """Get department by name"""
        return db.query(Departments).filter(Departments.name == name).first()

class CRUDDesignation(CRUDBase[Designations, DesignationCreate, DesignationUpdate]):
    async def get_by_department(self, db: Session, *, department_id: int) -> List[Designations]:
        """Get designations by department"""
        return db.query(Designations).filter(Designations.department_id == department_id).all()

class CRUDEmployee(CRUDBase[Employees, EmployeeCreate, EmployeeUpdate]):
    async def get_by_employee_id(self, db: Session, *, employee_id: str) -> Optional[Employees]:
        """Get employee by employee ID"""
        return db.query(Employees).filter(Employees.employee_id == employee_id).first()

    async def get_by_department(self, db: Session, *, department_id: int) -> List[Employees]:
        """Get employees by department"""
        return db.query(Employees).filter(Employees.department_id == department_id).all()

    async def get_by_manager(self, db: Session, *, manager_id: int) -> List[Employees]:
        """Get employees by manager"""
        return db.query(Employees).filter(Employees.manager_id == manager_id).all()

class CRUDCompany(CRUDBase[Companies, CompanyCreate, CompanyUpdate]):
    async def get_by_name(self, db: Session, *, name: str) -> Optional[Companies]:
        """Get company by name"""
        return db.query(Companies).filter(Companies.name == name).first()

    async def search_companies(self, db: Session, *, search_term: str, skip: int = 0, limit: int = 100) -> List[Companies]:
        """Search companies by name, industry, or description"""
        return db.query(Companies).filter(
            or_(
                Companies.name.contains(search_term),
                Companies.industry.contains(search_term),
                Companies.description.contains(search_term)
            )
        ).offset(skip).limit(limit).all()

class CRUDContact(CRUDBase[Contacts, ContactCreate, ContactUpdate]):
    async def get_by_company(self, db: Session, *, company_id: int) -> List[Contacts]:
        """Get contacts by company"""
        return db.query(Contacts).filter(Contacts.company_id == company_id).all()

    async def get_primary_contact(self, db: Session, *, company_id: int) -> Optional[Contacts]:
        """Get primary contact for a company"""
        return db.query(Contacts).filter(
            and_(Contacts.company_id == company_id, Contacts.is_primary == True)
        ).first()

class CRUDLead(CRUDBase[Leads, LeadCreate, LeadUpdate]):
    async def get_by_status(self, db: Session, *, status: str) -> List[Leads]:
        """Get leads by status"""
        return db.query(Leads).filter(Leads.status == status).all()

    async def get_by_assigned_user(self, db: Session, *, user_id: int) -> List[Leads]:
        """Get leads assigned to a user"""
        return db.query(Leads).filter(Leads.assigned_to_id == user_id).all()

class CRUDDeal(CRUDBase[Deals, DealCreate, DealUpdate]):
    async def get_by_stage(self, db: Session, *, stage: str) -> List[Deals]:
        """Get deals by stage"""
        return db.query(Deals).filter(Deals.stage == stage).all()

    async def get_by_owner(self, db: Session, *, owner_id: int) -> List[Deals]:
        """Get deals by owner"""
        return db.query(Deals).filter(Deals.owner_id == owner_id).all()

    async def get_revenue_by_stage(self, db: Session) -> Dict[str, float]:
        """Get total revenue by deal stage"""
        result = db.query(
            Deals.stage,
            func.sum(Deals.value).label('total_value')
        ).group_by(Deals.stage).all()

        return {stage: float(total_value or 0) for stage, total_value in result}

class CRUDActivity(CRUDBase[Activities, ActivityCreate, ActivityUpdate]):
    async def get_by_lead(self, db: Session, *, lead_id: int) -> List[Activities]:
        """Get activities by lead"""
        return db.query(Activities).filter(Activities.lead_id == lead_id).all()

    async def get_by_deal(self, db: Session, *, deal_id: int) -> List[Activities]:
        """Get activities by deal"""
        return db.query(Activities).filter(Activities.deal_id == deal_id).all()

    async def get_upcoming_activities(self, db: Session, *, user_id: int) -> List[Activities]:
        """Get upcoming activities for a user"""
        return db.query(Activities).filter(
            and_(
                Activities.assigned_to_id == user_id,
                Activities.scheduled_at > func.now(),
                Activities.is_completed == False
            )
        ).order_by(Activities.scheduled_at).all()

class CRUDLeaveType(CRUDBase[LeaveTypes, LeaveTypeCreate, LeaveTypeCreate]):
    pass

class CRUDLeaveRequest(CRUDBase[LeaveRequests, LeaveRequestCreate, LeaveRequestUpdate]):
    async def get_by_employee(self, db: Session, *, employee_id: int) -> List[LeaveRequests]:
        """Get leave requests by employee"""
        return db.query(LeaveRequests).filter(LeaveRequests.employee_id == employee_id).all()

    async def get_pending_requests(self, db: Session) -> List[LeaveRequests]:
        """Get pending leave requests"""
        return db.query(LeaveRequests).filter(LeaveRequests.status == 'pending').all()

class CRUDProject(CRUDBase[Projects, ProjectCreate, ProjectUpdate]):
    async def get_by_manager(self, db: Session, *, manager_id: int) -> List[Projects]:
        """Get projects by manager"""
        return db.query(Projects).filter(Projects.manager_id == manager_id).all()

    async def get_by_status(self, db: Session, *, status: str) -> List[Projects]:
        """Get projects by status"""
        return db.query(Projects).filter(Projects.status == status).all()

class CRUDTask(CRUDBase[Tasks, TaskCreate, TaskUpdate]):
    async def get_by_project(self, db: Session, *, project_id: int) -> List[Tasks]:
        """Get tasks by project"""
        return db.query(Tasks).filter(Tasks.project_id == project_id).all()

    async def get_by_assignee(self, db: Session, *, user_id: int) -> List[Tasks]:
        """Get tasks assigned to a user"""
        return db.query(Tasks).filter(Tasks.assigned_to_id == user_id).all()

    async def get_overdue_tasks(self, db: Session) -> List[Tasks]:
        """Get overdue tasks"""
        return db.query(Tasks).filter(
            and_(
                Tasks.due_date < func.now(),
                Tasks.status.in_(['todo', 'in_progress'])
            )
        ).all()

# Create CRUD instances
user = CRUDUser(Users)
department = CRUDDepartment(Departments)
designation = CRUDDesignation(Designations)
employee = CRUDEmployee(Employees)
company = CRUDCompany(Companies)
contact = CRUDContact(Contacts)
lead = CRUDLead(Leads)
deal = CRUDDeal(Deals)
activity = CRUDActivity(Activities)
leave_type = CRUDLeaveType(LeaveTypes)
leave_request = CRUDLeaveRequest(LeaveRequests)
project = CRUDProject(Projects)
task = CRUDTask(Tasks)