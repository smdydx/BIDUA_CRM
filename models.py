
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Decimal, Date, Time, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base = declarative_base()

# Enums for better data integrity
class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    HR = "hr"
    SALES = "sales"
    SUPPORT = "support"

class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class DealStage(enum.Enum):
    PROSPECTING = "prospecting"
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"

class LeaveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"

class PayrollStatus(enum.Enum):
    DRAFT = "draft"
    PROCESSED = "processed"
    PAID = "paid"

# Core User Management
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees", back_populates="user", uselist=False)
    created_leads = relationship("Leads", back_populates="created_by")
    assigned_leads = relationship("Leads", foreign_keys="Leads.assigned_to_id", back_populates="assigned_to")

# Company Structure
class Departments(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    manager_id = Column(Integer, ForeignKey("employees.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    manager = relationship("Employees", foreign_keys=[manager_id])
    employees = relationship("Employees", back_populates="department", foreign_keys="Employees.department_id")

class Designations(Base):
    __tablename__ = "designations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    level = Column(Integer)  # Hierarchy level
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    department = relationship("Departments")
    employees = relationship("Employees", back_populates="designation")

# HR Management
class Employees(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"))
    
    # Personal Information
    date_of_birth = Column(Date)
    gender = Column(String(10))
    marital_status = Column(String(20))
    address = Column(Text)
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    
    # Employment Details
    hire_date = Column(Date, nullable=False)
    employment_type = Column(String(20))  # Full-time, Part-time, Contract
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    salary = Column(Decimal(10, 2))
    termination_date = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("Users", back_populates="employee")
    department = relationship("Departments", back_populates="employees", foreign_keys=[department_id])
    designation = relationship("Designations", back_populates="employees")
    manager = relationship("Employees", remote_side=[id])
    subordinates = relationship("Employees", back_populates="manager")
    
    # HR related relationships
    leave_requests = relationship("LeaveRequests", back_populates="employee")
    attendance_records = relationship("Attendance", back_populates="employee")
    payroll_records = relationship("Payroll", back_populates="employee")

# CRM - Customer Management
class Companies(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    industry = Column(String(100))
    size = Column(String(50))  # Small, Medium, Large, Enterprise
    website = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    annual_revenue = Column(Decimal(15, 2))
    description = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    contacts = relationship("Contacts", back_populates="company")
    leads = relationship("Leads", back_populates="company")
    deals = relationship("Deals", back_populates="company")

class Contacts(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    job_title = Column(String(100))
    department = Column(String(100))
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Companies", back_populates="contacts")
    leads = relationship("Leads", back_populates="contact")
    deals = relationship("Deals", back_populates="contact")

# CRM - Sales Pipeline
class Leads(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    source = Column(String(100))  # Website, Email, Phone, Referral, etc.
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    estimated_value = Column(Decimal(12, 2))
    probability = Column(Integer, default=0)  # 0-100%
    expected_close_date = Column(Date)
    
    # Assignment
    created_by_id = Column(Integer, ForeignKey("users.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    
    # Notes and tracking
    description = Column(Text)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Companies", back_populates="leads")
    contact = relationship("Contacts", back_populates="leads")
    created_by = relationship("Users", foreign_keys=[created_by_id], back_populates="created_leads")
    assigned_to = relationship("Users", foreign_keys=[assigned_to_id], back_populates="assigned_leads")
    activities = relationship("Activities", back_populates="lead")

class Deals(Base):
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"))
    
    stage = Column(Enum(DealStage), default=DealStage.PROSPECTING)
    value = Column(Decimal(12, 2), nullable=False)
    probability = Column(Integer, default=0)  # 0-100%
    expected_close_date = Column(Date)
    actual_close_date = Column(Date)
    
    # Assignment
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    description = Column(Text)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Companies", back_populates="deals")
    contact = relationship("Contacts", back_populates="deals")
    lead = relationship("Leads")
    owner = relationship("Users")
    activities = relationship("Activities", back_populates="deal")

# Activity Tracking
class Activities(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # Call, Email, Meeting, Task, Note
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Related entities
    lead_id = Column(Integer, ForeignKey("leads.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    is_completed = Column(Boolean, default=False)
    
    # Assignment
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lead = relationship("Leads", back_populates="activities")
    deal = relationship("Deals", back_populates="activities")
    contact = relationship("Contacts")
    assigned_to = relationship("Users", foreign_keys=[assigned_to_id])
    created_by = relationship("Users", foreign_keys=[created_by_id])

# HR - Leave Management
class LeaveTypes(Base):
    __tablename__ = "leave_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    max_days_per_year = Column(Integer)
    is_paid = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    leave_requests = relationship("LeaveRequests", back_populates="leave_type")

class LeaveRequests(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"))
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_requested = Column(Integer, nullable=False)
    reason = Column(Text)
    
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    approval_date = Column(DateTime(timezone=True))
    approval_comments = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees", back_populates="leave_requests")
    leave_type = relationship("LeaveTypes", back_populates="leave_requests")
    approved_by = relationship("Users")

# HR - Attendance Management
class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, nullable=False)
    
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    break_duration_minutes = Column(Integer, default=0)
    total_hours = Column(Decimal(4, 2))
    
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees", back_populates="attendance_records")

# HR - Payroll Management
class Payroll(Base):
    __tablename__ = "payroll"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    
    # Pay period
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    
    # Salary components
    basic_salary = Column(Decimal(10, 2), nullable=False)
    allowances = Column(Decimal(10, 2), default=0)
    overtime_amount = Column(Decimal(10, 2), default=0)
    bonus = Column(Decimal(10, 2), default=0)
    
    # Deductions
    tax_deduction = Column(Decimal(10, 2), default=0)
    insurance_deduction = Column(Decimal(10, 2), default=0)
    other_deductions = Column(Decimal(10, 2), default=0)
    
    # Totals
    gross_pay = Column(Decimal(10, 2), nullable=False)
    net_pay = Column(Decimal(10, 2), nullable=False)
    
    status = Column(Enum(PayrollStatus), default=PayrollStatus.DRAFT)
    processed_by_id = Column(Integer, ForeignKey("users.id"))
    processed_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees", back_populates="payroll_records")
    processed_by = relationship("Users")

# System Configuration
class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    category = Column(String(50))  # CRM, HR, System
    is_public = Column(Boolean, default=False)  # Can be accessed by non-admin users
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Audit Trail
class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # CREATE, UPDATE, DELETE
    old_values = Column(Text)  # JSON string of old values
    new_values = Column(Text)  # JSON string of new values
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")
