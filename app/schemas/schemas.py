from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Union
from datetime import datetime, date, time
from decimal import Decimal
import enum
from app.models.models import (
    UserRole, LeadStatus, DealStage, EmployeeStatus, 
    LeaveStatus, AttendanceStatus, PayrollStatus,
    ProjectStatus, TaskStatus
)

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# User Management Schemas
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.EMPLOYEE
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

# Department Schemas
class DepartmentBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None

class DepartmentUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None
    is_active: Optional[bool] = None

class DepartmentResponse(DepartmentBase):
    id: int
    manager_id: Optional[int]
    created_at: datetime

# Designation Schemas
class DesignationBase(BaseSchema):
    title: str = Field(..., max_length=100)
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True

class DesignationCreate(DesignationBase):
    department_id: int

class DesignationUpdate(BaseSchema):
    title: Optional[str] = None
    department_id: Optional[int] = None
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DesignationResponse(DesignationBase):
    id: int
    department_id: int
    created_at: datetime

# Employee Schemas
class EmployeeBase(BaseSchema):
    employee_id: str = Field(..., pattern=r'^EMP\d{3,6}$')
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    marital_status: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    emergency_contact: Optional[str] = Field(None, max_length=100)
    emergency_phone: Optional[str] = Field(None, max_length=20)
    emergency_relationship: Optional[str] = Field(None, max_length=50)
    blood_group: Optional[str] = Field(None, max_length=10)
    nationality: Optional[str] = Field(None, max_length=100)
    hire_date: date
    employment_type: Optional[str] = Field(None, max_length=20)
    work_location: Optional[str] = Field(None, max_length=100)
    shift_timing: Optional[str] = Field(None, max_length=50)
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    salary: Optional[Decimal] = Field(None, ge=0, le=10000000)

class EmployeeCreate(EmployeeBase):
    user_id: int
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    manager_id: Optional[int] = None

class EmployeeUpdate(BaseSchema):
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    manager_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    employment_type: Optional[str] = None
    status: Optional[EmployeeStatus] = None
    salary: Optional[Decimal] = None

class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    department_id: Optional[int]
    designation_id: Optional[int]
    manager_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Company Schemas
class CompanyBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = Field(None, pattern=r'^(Small|Medium|Large|Enterprise)$')
    website: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    annual_revenue: Optional[Decimal] = Field(None, ge=0)
    employee_count: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseSchema):
    name: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None

class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

# Contact Schemas
class ContactBase(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    mobile: Optional[str] = Field(None, max_length=20)
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    is_primary: bool = False
    is_active: bool = True

class ContactCreate(ContactBase):
    company_id: int

class ContactUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    is_primary: Optional[bool] = None
    is_active: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    company_id: int
    created_at: datetime
    updated_at: Optional[datetime]

# Lead Schemas
class LeadBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=200)
    source: Optional[str] = Field(None, max_length=100)
    status: LeadStatus = LeadStatus.NEW
    estimated_value: Optional[Decimal] = Field(None, ge=0)
    probability: int = Field(0, ge=0, le=100)
    expected_close_date: Optional[date] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    assigned_to_id: Optional[int] = None

class LeadUpdate(BaseSchema):
    title: Optional[str] = None
    status: Optional[LeadStatus] = None
    estimated_value: Optional[Decimal] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    expected_close_date: Optional[date] = None
    assigned_to_id: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class LeadResponse(LeadBase):
    id: int
    company_id: Optional[int]
    contact_id: Optional[int]
    created_by_id: Optional[int]
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Deal Schemas
class DealBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=200)
    stage: DealStage = DealStage.PROSPECTING
    value: Decimal = Field(..., gt=0, le=100000000)
    probability: int = Field(0, ge=0, le=100)
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class DealCreate(DealBase):
    company_id: int
    contact_id: Optional[int] = None
    lead_id: Optional[int] = None
    owner_id: Optional[int] = None

class DealUpdate(BaseSchema):
    title: Optional[str] = None
    stage: Optional[DealStage] = None
    value: Optional[Decimal] = Field(None, gt=0, le=100000000)
    probability: Optional[int] = Field(None, ge=0, le=100)
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    owner_id: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class DealResponse(DealBase):
    id: int
    company_id: int
    contact_id: Optional[int]
    lead_id: Optional[int]
    owner_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Activity Schemas
class ActivityBase(BaseSchema):
    type: str = Field(..., max_length=50)
    subject: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    is_completed: bool = False

class ActivityCreate(ActivityBase):
    lead_id: Optional[int] = None
    deal_id: Optional[int] = None
    contact_id: Optional[int] = None
    assigned_to_id: Optional[int] = None

class ActivityUpdate(BaseSchema):
    type: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    is_completed: Optional[bool] = None
    assigned_to_id: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    lead_id: Optional[int]
    deal_id: Optional[int]
    contact_id: Optional[int]
    assigned_to_id: Optional[int]
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Leave Schemas
class LeaveTypeBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    max_days_per_year: Optional[int] = Field(None, ge=0)
    is_active: bool = True

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeResponse(LeaveTypeBase):
    id: int
    created_at: datetime

class LeaveRequestBase(BaseSchema):
    start_date: date
    end_date: date
    days_requested: int = Field(..., ge=1)
    reason: str = Field(..., min_length=10)
    status: LeaveStatus = LeaveStatus.PENDING

class LeaveRequestCreate(LeaveRequestBase):
    leave_type_id: int

class LeaveRequestUpdate(BaseSchema):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_requested: Optional[int] = Field(None, ge=1)
    reason: Optional[str] = None
    status: Optional[LeaveStatus] = None

class LeaveRequestResponse(LeaveRequestBase):
    id: int
    leave_type_id: int
    employee_id: int
    approved_by_id: Optional[int]
    approved_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

# Project Schemas
class ProjectBase(BaseSchema):
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = Field(None, ge=0)
    status: ProjectStatus = ProjectStatus.PLANNING

class ProjectCreate(ProjectBase):
    client_id: Optional[int] = None
    manager_id: Optional[int] = None

class ProjectUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    status: Optional[ProjectStatus] = None
    manager_id: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    client_id: Optional[int]
    manager_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Task Schemas
class TaskBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(None, pattern=r'^(Low|Medium|High|Critical)$')
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: Optional[int] = Field(None, ge=0)
    actual_hours: Optional[int] = Field(None, ge=0)

class TaskCreate(TaskBase):
    project_id: int
    assigned_to_id: Optional[int] = None

class TaskUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[TaskStatus] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    assigned_to_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    project_id: int
    assigned_to_id: Optional[int]
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

# Pagination Schema
class PaginatedResponse(BaseSchema):
    items: List[BaseSchema]
    total: int
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)
    pages: int

# Common Response Schemas
class MessageResponse(BaseSchema):
    message: str
    success: bool = True

class ErrorResponse(BaseSchema):
    error: str
    detail: Optional[str] = None
    success: bool = False

# Authentication Schemas
class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseSchema):
    username: Optional[str] = None
    user_id: Optional[int] = None

class LoginRequest(BaseSchema):
    username: str
    password: str