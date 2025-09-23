from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.core.database import get_db, engine
from app.models.models import Base
from app.middleware.middleware import add_all_middleware
import app.crud.crud as crud
import app.schemas.schemas as schemas
import uvicorn
import asyncio

# Create FastAPI app
app = FastAPI(
    title="CRM + HRMS System",
    description="Comprehensive Customer Relationship Management and Human Resource Management System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all custom middleware
add_all_middleware(app)

# Security
security = HTTPBearer(auto_error=False)

# Create database tables
@app.on_event("startup")
async def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

@app.get("/")
async def root():
    return {
        "message": "Welcome to CRM + HRMS System",
        "status": "active",
        "features": [
            "Customer Relationship Management",
            "Human Resource Management", 
            "Project Management",
            "Task Management",
            "Training & Development",
            "Expense Management",
            "Document Management",
            "Email Campaigns",
            "Support Ticketing",
            "Inventory Management",
            "Financial Management"
        ]
    }

# Authentication helper
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    # TODO: Implement JWT token validation
    # For now, return a mock user or implement simple authentication
    user = await crud.user.get_by_username(db, username="admin")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

# Pagination helper
def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
):
    return {"skip": (page - 1) * size, "limit": size, "page": page, "size": size}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# ==================== USER MANAGEMENT ENDPOINTS ====================

@app.post("/auth/login", response_model=schemas.Token)
async def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint"""
    user = await crud.user.authenticate(db, email=login_data.username, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    # TODO: Generate JWT token
    return {
        "access_token": "mock_token_" + user.username,
        "token_type": "bearer",
        "expires_in": 3600
    }

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new user"""
    # Check if user already exists
    existing_user = await crud.user.get_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_username = await crud.user.get_by_username(db, username=user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    return await crud.user.create(db, obj_in=user)

@app.get("/users/", response_model=List[schemas.UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search term"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all users with pagination and filtering"""
    filters = {}
    if role:
        filters['role'] = role
    if is_active is not None:
        filters['is_active'] = is_active

    users = await crud.user.get_multi(
        db, 
        skip=pagination["skip"], 
        limit=pagination["limit"],
        filters=filters,
        search=search
    )
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get user by ID"""
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update user"""
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return await crud.user.update(db, db_obj=user, obj_in=user_update)

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Soft delete user"""
    user = await crud.user.soft_delete(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully", "success": True}

# ==================== HR MANAGEMENT ENDPOINTS ====================

# Department endpoints
@app.post("/departments/", response_model=schemas.DepartmentResponse)
async def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new department"""
    existing = await crud.department.get_by_name(db, name=department.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name already exists"
        )
    return await crud.department.create(db, obj_in=department)

@app.get("/departments/", response_model=List[schemas.DepartmentResponse])
async def get_departments(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all departments"""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    return await crud.department.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/departments/{department_id}", response_model=schemas.DepartmentResponse)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get department by ID"""
    department = await crud.department.get(db, id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@app.put("/departments/{department_id}", response_model=schemas.DepartmentResponse)
async def update_department(
    department_id: int,
    department_update: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update department"""
    department = await crud.department.get(db, id=department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return await crud.department.update(db, db_obj=department, obj_in=department_update)

# Designation endpoints
@app.post("/designations/", response_model=schemas.DesignationResponse)
async def create_designation(
    designation: schemas.DesignationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new designation"""
    return await crud.designation.create(db, obj_in=designation)

@app.get("/designations/", response_model=List[schemas.DesignationResponse])
async def get_designations(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    department_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all designations"""
    filters = {}
    if department_id:
        filters['department_id'] = department_id
    if is_active is not None:
        filters['is_active'] = is_active

    return await crud.designation.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Employee endpoints
@app.post("/employees/", response_model=schemas.EmployeeResponse)
async def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new employee"""
    existing = await crud.employee.get_by_employee_id(db, employee_id=employee.employee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    return await crud.employee.create(db, obj_in=employee)

@app.get("/employees/", response_model=List[schemas.EmployeeResponse])
async def get_employees(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    department_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    manager_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all employees with filtering"""
    filters = {}
    if department_id:
        filters['department_id'] = department_id
    if status:
        filters['status'] = status
    if manager_id:
        filters['manager_id'] = manager_id

    return await crud.employee.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get employee by ID"""
    employee = await crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update employee"""
    employee = await crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await crud.employee.update(db, db_obj=employee, obj_in=employee_update)

# Leave Type endpoints
@app.post("/leave-types/", response_model=schemas.LeaveTypeResponse)
async def create_leave_type(
    leave_type: schemas.LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new leave type"""
    return await crud.leave_type.create(db, obj_in=leave_type)

@app.get("/leave-types/", response_model=List[schemas.LeaveTypeResponse])
async def get_leave_types(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    is_active: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all leave types"""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    return await crud.leave_type.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Leave Request endpoints
@app.post("/leave-requests/", response_model=schemas.LeaveRequestResponse)
async def create_leave_request(
    leave_request: schemas.LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new leave request"""
    return await crud.leave_request.create(db, obj_in=leave_request, created_by_id=current_user.id)

@app.get("/leave-requests/", response_model=List[schemas.LeaveRequestResponse])
async def get_leave_requests(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    employee_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get leave requests with filtering"""
    filters = {}
    if employee_id:
        filters['employee_id'] = employee_id
    if status:
        filters['status'] = status

    return await crud.leave_request.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.put("/leave-requests/{request_id}/approve")
async def approve_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Approve a leave request"""
    leave_request = await crud.leave_request.get(db, id=request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    update_data = {"status": "approved", "approved_by_id": current_user.id}
    await crud.leave_request.update(db, db_obj=leave_request, obj_in=update_data)
    return {"message": "Leave request approved", "success": True}

# ==================== CRM ENDPOINTS ====================

# Company endpoints
@app.post("/companies/", response_model=schemas.CompanyResponse)
async def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new company"""
    existing = await crud.company.get_by_name(db, name=company.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company name already exists"
        )
    return await crud.company.create(db, obj_in=company)

@app.get("/companies/", response_model=List[schemas.CompanyResponse])
async def get_companies(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get all companies with search and filtering"""
    filters = {}
    if industry:
        filters['industry'] = industry
    if size:
        filters['size'] = size

    return await crud.company.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], 
        filters=filters, search=search
    )

@app.get("/companies/{company_id}", response_model=schemas.CompanyResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get company by ID"""
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.put("/companies/{company_id}", response_model=schemas.CompanyResponse)
async def update_company(
    company_id: int,
    company_update: schemas.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update company"""
    company = await crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return await crud.company.update(db, db_obj=company, obj_in=company_update)

# Contact endpoints
@app.post("/contacts/", response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new contact"""
    return await crud.contact.create(db, obj_in=contact)

@app.get("/contacts/", response_model=List[schemas.ContactResponse])
async def get_contacts(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    company_id: Optional[int] = Query(None),
    is_primary: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get contacts with filtering"""
    filters = {}
    if company_id:
        filters['company_id'] = company_id
    if is_primary is not None:
        filters['is_primary'] = is_primary

    return await crud.contact.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Lead endpoints
@app.post("/leads/", response_model=schemas.LeadResponse)
async def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new lead"""
    return await crud.lead.create(db, obj_in=lead, created_by_id=current_user.id)

@app.get("/leads/", response_model=List[schemas.LeadResponse])
async def get_leads(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = Query(None),
    assigned_to_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get leads with filtering"""
    filters = {}
    if status:
        filters['status'] = status
    if assigned_to_id:
        filters['assigned_to_id'] = assigned_to_id

    return await crud.lead.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

# Deal endpoints
@app.post("/deals/", response_model=schemas.DealResponse)
async def create_deal(
    deal: schemas.DealCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new deal"""
    return await crud.deal.create(db, obj_in=deal, created_by_id=current_user.id)

@app.get("/deals/", response_model=List[schemas.DealResponse])
async def get_deals(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    stage: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get deals with filtering"""
    filters = {}
    if stage:
        filters['stage'] = stage
    if owner_id:
        filters['owner_id'] = owner_id

    return await crud.deal.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/deals/revenue/by-stage")
async def get_revenue_by_stage(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get revenue breakdown by deal stage"""
    return await crud.deal.get_revenue_by_stage(db)

# Activity endpoints
@app.post("/activities/", response_model=schemas.ActivityResponse)
async def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new activity"""
    return await crud.activity.create(db, obj_in=activity, created_by_id=current_user.id)

@app.get("/activities/", response_model=List[schemas.ActivityResponse])
async def get_activities(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    lead_id: Optional[int] = Query(None),
    deal_id: Optional[int] = Query(None),
    is_completed: Optional[bool] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get activities with filtering"""
    filters = {}
    if lead_id:
        filters['lead_id'] = lead_id
    if deal_id:
        filters['deal_id'] = deal_id
    if is_completed is not None:
        filters['is_completed'] = is_completed

    return await crud.activity.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/activities/upcoming")
async def get_upcoming_activities(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get upcoming activities for current user"""
    return await crud.activity.get_upcoming_activities(db, user_id=current_user.id)

# ==================== PROJECT MANAGEMENT ENDPOINTS ====================

# Project endpoints
@app.post("/projects/", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new project"""
    return await crud.project.create(db, obj_in=project, created_by_id=current_user.id)

@app.get("/projects/", response_model=List[schemas.ProjectResponse])
async def get_projects(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = Query(None),
    manager_id: Optional[int] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get projects with filtering"""
    filters = {}
    if status:
        filters['status'] = status
    if manager_id:
        filters['manager_id'] = manager_id

    return await crud.project.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get project by ID"""
    project = await crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Task endpoints
@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Create a new task"""
    return await crud.task.create(db, obj_in=task, created_by_id=current_user.id)

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
async def get_tasks(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    project_id: Optional[int] = Query(None),
    assigned_to_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get tasks with filtering"""
    filters = {}
    if project_id:
        filters['project_id'] = project_id
    if assigned_to_id:
        filters['assigned_to_id'] = assigned_to_id
    if status:
        filters['status'] = status
    if priority:
        filters['priority'] = priority

    return await crud.task.get_multi(
        db, skip=pagination["skip"], limit=pagination["limit"], filters=filters
    )

@app.get("/tasks/overdue")
async def get_overdue_tasks(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get overdue tasks"""
    return await crud.task.get_overdue_tasks(db)

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Update task"""
    task = await crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.task.update(db, db_obj=task, obj_in=task_update)

# ==================== ANALYTICS ENDPOINTS ====================

@app.get("/analytics/dashboard")
async def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    """Get dashboard analytics summary"""
    # Count various entities
    total_users = await crud.user.get_count(db)
    total_employees = await crud.employee.get_count(db)
    total_companies = await crud.company.get_count(db)
    total_leads = await crud.lead.get_count(db)
    total_deals = await crud.deal.get_count(db)
    total_projects = await crud.project.get_count(db)
    total_tasks = await crud.task.get_count(db)

    # Get revenue by stage
    revenue_by_stage = await crud.deal.get_revenue_by_stage(db)

    return {
        "total_users": total_users,
        "total_employees": total_employees,
        "total_companies": total_companies,
        "total_leads": total_leads,
        "total_deals": total_deals,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "revenue_by_stage": revenue_by_stage
    }

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(hr.router, prefix="/hr", tags=["HR Management"])
app.include_router(crm.router, prefix="/crm", tags=["CRM"])
app.include_router(projects.router, prefix="/projects", tags=["Project Management"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True
    )