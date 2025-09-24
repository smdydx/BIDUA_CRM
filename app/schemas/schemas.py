
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, EmailStr, validator
from enum import Enum

# Enum classes for validation
class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"
    MANAGER = "manager"

class LeadStatusEnum(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"

class DealStageEnum(str, Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRoleEnum
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

# Department schemas
class DepartmentBase(BaseSchema):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

# Designation schemas
class DesignationBase(BaseSchema):
    title: str
    description: Optional[str] = None
    department_id: int
    is_active: bool = True

class DesignationCreate(DesignationBase):
    pass

class DesignationUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None

class DesignationResponse(DesignationBase):
    id: int
    created_at: datetime

# Employee schemas
class EmployeeBase(BaseSchema):
    employee_id: str
    user_id: int
    department_id: int
    designation_id: int
    manager_id: Optional[int] = None
    hire_date: date
    salary: Optional[Decimal] = None
    status: str = "active"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseSchema):
    employee_id: Optional[str] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    manager_id: Optional[int] = None
    hire_date: Optional[date] = None
    salary: Optional[Decimal] = None
    status: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime

# Company schemas
class CompanyBase(BaseSchema):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseSchema):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime

# Contact schemas
class ContactBase(BaseSchema):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: int
    is_primary: bool = False

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None
    is_primary: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    created_at: datetime

# Lead schemas
class LeadBase(BaseSchema):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: LeadStatusEnum = LeadStatusEnum.NEW
    source: Optional[str] = None
    assigned_to_id: Optional[int] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[LeadStatusEnum] = None
    source: Optional[str] = None
    assigned_to_id: Optional[int] = None

class LeadResponse(LeadBase):
    id: int
    created_at: datetime

# Deal schemas
class DealBase(BaseSchema):
    title: str
    value: Decimal
    stage: DealStageEnum
    company_id: int
    contact_id: Optional[int] = None
    owner_id: int
    expected_close_date: Optional[date] = None
    description: Optional[str] = None

class DealCreate(DealBase):
    pass

class DealUpdate(BaseSchema):
    title: Optional[str] = None
    value: Optional[Decimal] = None
    stage: Optional[DealStageEnum] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    owner_id: Optional[int] = None
    expected_close_date: Optional[date] = None
    description: Optional[str] = None

class DealResponse(DealBase):
    id: int
    created_at: datetime

# Activity schemas
class ActivityBase(BaseSchema):
    title: str
    description: Optional[str] = None
    activity_type: str
    scheduled_at: datetime
    assigned_to_id: int
    lead_id: Optional[int] = None
    deal_id: Optional[int] = None
    is_completed: bool = False

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    activity_type: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    assigned_to_id: Optional[int] = None
    lead_id: Optional[int] = None
    deal_id: Optional[int] = None
    is_completed: Optional[bool] = None

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime

# Leave Type schemas
class LeaveTypeBase(BaseSchema):
    name: str
    days_allowed: int
    is_active: bool = True

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeResponse(LeaveTypeBase):
    id: int
    created_at: datetime

# Leave Request schemas
class LeaveRequestBase(BaseSchema):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: str = "pending"

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseSchema):
    status: Optional[str] = None
    reason: Optional[str] = None

class LeaveRequestResponse(LeaveRequestBase):
    id: int
    created_at: datetime

# Project schemas
class ProjectBase(BaseSchema):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    manager_id: int
    status: str = "planning"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    manager_id: Optional[int] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

# Task schemas
class TaskBase(BaseSchema):
    title: str
    description: Optional[str] = None
    project_id: int
    assigned_to_id: int
    due_date: date
    priority: str = "medium"
    status: str = "todo"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
