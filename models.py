
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Decimal, Date, Time, Enum, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
import enum
import re
from datetime import datetime, date
from decimal import Decimal as PyDecimal

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

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectStatus(enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

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
    
    # Table constraints
    __table_args__ = (
        CheckConstraint("length(username) >= 3", name="check_username_length"),
        CheckConstraint("length(first_name) >= 2", name="check_first_name_length"),
        CheckConstraint("length(last_name) >= 2", name="check_last_name_length"),
        Index('idx_users_email_active', 'email', 'is_active'),
    )
    
    # Validation methods
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email is required")
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")
        return email.lower()
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return username.lower()
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if phone:
            # Remove all non-digit characters for validation
            digits_only = re.sub(r'\D', '', phone)
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError("Phone number must be between 10-15 digits")
        return phone
    
    @validates('first_name', 'last_name')
    def validate_names(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError(f"{key.replace('_', ' ').title()} must be at least 2 characters long")
        if not re.match("^[a-zA-Z\s]+$", name):
            raise ValueError(f"{key.replace('_', ' ').title()} can only contain letters and spaces")
        return name.strip().title()
    
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
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    emergency_relationship = Column(String(50))
    blood_group = Column(String(10))
    nationality = Column(String(100))
    
    # Official Documents
    aadhar_number = Column(String(20))  # Indian ID
    pan_number = Column(String(20))     # Indian Tax ID
    passport_number = Column(String(50))
    driving_license = Column(String(50))
    
    # Bank Details
    bank_name = Column(String(100))
    bank_account_number = Column(String(50))
    bank_ifsc_code = Column(String(20))
    bank_branch = Column(String(100))
    
    # Employment Details
    hire_date = Column(Date, nullable=False)
    probation_period_months = Column(Integer, default=6)
    confirmation_date = Column(Date)
    employment_type = Column(String(20))  # Full-time, Part-time, Contract
    work_location = Column(String(100))
    shift_timing = Column(String(50))
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    salary = Column(Decimal(10, 2))
    termination_date = Column(Date)
    termination_reason = Column(Text)
    
    # Skills and Qualifications
    skills = Column(Text)  # JSON string
    education = Column(Text)  # JSON string
    certifications = Column(Text)  # JSON string
    experience_years = Column(Integer)
    
    # Profile
    profile_picture_url = Column(String(500))
    biography = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Table constraints
    __table_args__ = (
        CheckConstraint("hire_date <= CURRENT_DATE", name="check_hire_date_not_future"),
        CheckConstraint("termination_date >= hire_date", name="check_termination_after_hire"),
        CheckConstraint("confirmation_date >= hire_date", name="check_confirmation_after_hire"),
        CheckConstraint("probation_period_months >= 0", name="check_probation_positive"),
        CheckConstraint("salary >= 0", name="check_salary_positive"),
        CheckConstraint("experience_years >= 0", name="check_experience_positive"),
        CheckConstraint("manager_id != id", name="check_not_self_manager"),
        CheckConstraint("employment_type IN ('Full-time', 'Part-time', 'Contract', 'Intern')", name="check_employment_type"),
        Index('idx_employees_dept_status', 'department_id', 'status'),
        Index('idx_employees_manager', 'manager_id'),
    )
    
    # Validation methods
    @validates('employee_id')
    def validate_employee_id(self, key, employee_id):
        if not employee_id:
            raise ValueError("Employee ID is required")
        # Format: EMP001, EMP002, etc.
        if not re.match(r'^EMP\d{3,6}$', employee_id):
            raise ValueError("Employee ID must be in format EMP001, EMP002, etc.")
        return employee_id.upper()
    
    @validates('date_of_birth')
    def validate_date_of_birth(self, key, dob):
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18 or age > 100:
                raise ValueError("Employee age must be between 18 and 100 years")
        return dob
    
    @validates('hire_date')
    def validate_hire_date(self, key, hire_date):
        if hire_date and hire_date > date.today():
            raise ValueError("Hire date cannot be in the future")
        return hire_date
    
    @validates('aadhar_number')
    def validate_aadhar(self, key, aadhar):
        if aadhar:
            # Remove spaces and validate 12 digits
            aadhar_clean = re.sub(r'\s', '', aadhar)
            if not re.match(r'^\d{12}$', aadhar_clean):
                raise ValueError("Aadhar number must be 12 digits")
            return aadhar_clean
        return aadhar
    
    @validates('pan_number')
    def validate_pan(self, key, pan):
        if pan:
            pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
            if not pan_pattern.match(pan.upper()):
                raise ValueError("Invalid PAN number format")
            return pan.upper()
        return pan
    
    @validates('bank_ifsc_code')
    def validate_ifsc(self, key, ifsc):
        if ifsc:
            # Indian IFSC format: 4 letters + 7 alphanumeric
            ifsc_pattern = re.compile(r'^[A-Z]{4}[A-Z0-9]{7}$')
            if not ifsc_pattern.match(ifsc.upper()):
                raise ValueError("Invalid IFSC code format")
            return ifsc.upper()
        return ifsc
    
    @validates('salary')
    def validate_salary(self, key, salary):
        if salary is not None:
            if salary < 0:
                raise ValueError("Salary cannot be negative")
            if salary > 10000000:  # 1 crore max
                raise ValueError("Salary seems too high")
        return salary
    
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
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    annual_revenue = Column(Decimal(15, 2))
    employee_count = Column(Integer)
    description = Column(Text)
    logo_url = Column(String(500))
    linkedin_url = Column(String(255))
    facebook_url = Column(String(255))
    twitter_url = Column(String(255))
    gst_number = Column(String(50))  # For Indian businesses
    pan_number = Column(String(20))  # For Indian businesses
    company_registration_number = Column(String(100))
    is_active = Column(Boolean, default=True)
    tags = Column(Text)  # JSON string for tags
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Table constraints
    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="check_company_name_length"),
        CheckConstraint("employee_count >= 0", name="check_employee_count_positive"),
        CheckConstraint("annual_revenue >= 0", name="check_revenue_positive"),
        CheckConstraint("size IN ('Small', 'Medium', 'Large', 'Enterprise')", name="check_company_size"),
        Index('idx_companies_name_active', 'name', 'is_active'),
        Index('idx_companies_industry', 'industry'),
    )
    
    # Validation methods
    @validates('email')
    def validate_email(self, key, email):
        if email:
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(email):
                raise ValueError("Invalid email format")
            return email.lower()
        return email
    
    @validates('website')
    def validate_website(self, key, website):
        if website:
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not url_pattern.match(website):
                raise ValueError("Invalid website URL format")
        return website
    
    @validates('gst_number')
    def validate_gst(self, key, gst_number):
        if gst_number:
            # Indian GST format: 2 digits (state) + 10 digits (PAN) + 1 digit + 1 letter + 1 digit
            gst_pattern = re.compile(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$')
            if not gst_pattern.match(gst_number.upper()):
                raise ValueError("Invalid GST number format")
            return gst_number.upper()
        return gst_number
    
    @validates('pan_number')
    def validate_pan(self, key, pan_number):
        if pan_number:
            # Indian PAN format: 5 letters + 4 digits + 1 letter
            pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
            if not pan_pattern.match(pan_number.upper()):
                raise ValueError("Invalid PAN number format")
            return pan_number.upper()
        return pan_number
    
    @validates('annual_revenue', 'employee_count')
    def validate_positive_numbers(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be negative")
        return value
    
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
    
    # Table constraints
    __table_args__ = (
        CheckConstraint("value > 0", name="check_deal_value_positive"),
        CheckConstraint("probability >= 0 AND probability <= 100", name="check_probability_range"),
        CheckConstraint("expected_close_date >= CURRENT_DATE OR expected_close_date IS NULL", name="check_expected_date_future"),
        CheckConstraint("actual_close_date >= CURRENT_DATE OR actual_close_date IS NULL", name="check_actual_date_valid"),
        CheckConstraint("length(title) >= 3", name="check_deal_title_length"),
        Index('idx_deals_stage_owner', 'stage', 'owner_id'),
        Index('idx_deals_company_stage', 'company_id', 'stage'),
    )
    
    # Validation methods
    @validates('value')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError("Deal value is required")
        if value <= 0:
            raise ValueError("Deal value must be positive")
        if value > 100000000:  # 10 crore max
            raise ValueError("Deal value seems too high")
        return value
    
    @validates('probability')
    def validate_probability(self, key, probability):
        if probability is not None:
            if probability < 0 or probability > 100:
                raise ValueError("Probability must be between 0 and 100")
        return probability
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) < 3:
            raise ValueError("Deal title must be at least 3 characters long")
        return title.strip()
    
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
    
    # Table constraints
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_leave_end_after_start"),
        CheckConstraint("days_requested > 0", name="check_leave_days_positive"),
        CheckConstraint("start_date >= CURRENT_DATE", name="check_leave_start_future"),
        UniqueConstraint('employee_id', 'start_date', 'end_date', name='unique_employee_leave_period'),
        Index('idx_leave_requests_employee_status', 'employee_id', 'status'),
    )
    
    # Validation methods
    @validates('start_date', 'end_date')
    def validate_dates(self, key, value):
        if value and value < date.today():
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be in the past")
        return value
    
    @validates('days_requested')
    def validate_days(self, key, days):
        if days is None or days <= 0:
            raise ValueError("Days requested must be positive")
        if days > 365:
            raise ValueError("Cannot request more than 365 days")
        return days
    
    @validates('reason')
    def validate_reason(self, key, reason):
        if reason and len(reason.strip()) < 5:
            raise ValueError("Leave reason must be at least 5 characters long")
        return reason.strip() if reason else reason
    
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

# Project Management
class Projects(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Decimal(12, 2))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Companies")
    manager = relationship("Users")
    tasks = relationship("Tasks", back_populates="project")

class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    start_date = Column(Date)
    due_date = Column(Date)
    completed_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(String(20), default="medium")
    estimated_hours = Column(Decimal(5, 2))
    actual_hours = Column(Decimal(5, 2))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Projects", back_populates="tasks")
    assigned_to = relationship("Users", foreign_keys=[assigned_to_id])
    created_by = relationship("Users", foreign_keys=[created_by_id])

# Document Management
class Documents(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    
    # Related entities
    employee_id = Column(Integer, ForeignKey("employees.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    
    # Document categories
    category = Column(String(50))  # contract, resume, certificate, etc.
    is_confidential = Column(Boolean, default=False)
    
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    company = relationship("Companies")
    deal = relationship("Deals")
    uploaded_by = relationship("Users")

# Performance Management
class PerformanceReviews(Base):
    __tablename__ = "performance_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    
    # Ratings (1-5 scale)
    overall_rating = Column(Integer)
    technical_skills = Column(Integer)
    communication_skills = Column(Integer)
    teamwork = Column(Integer)
    leadership = Column(Integer)
    punctuality = Column(Integer)
    
    # Comments
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    goals_next_period = Column(Text)
    reviewer_comments = Column(Text)
    employee_comments = Column(Text)
    
    status = Column(String(20), default="draft")  # draft, submitted, approved
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees")
    reviewer = relationship("Users")

# Training Management
class TrainingPrograms(Base):
    __tablename__ = "training_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    trainer_name = Column(String(100))
    
    start_date = Column(Date)
    end_date = Column(Date)
    duration_hours = Column(Integer)
    max_participants = Column(Integer)
    cost_per_participant = Column(Decimal(10, 2))
    
    is_mandatory = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    enrollments = relationship("TrainingEnrollments", back_populates="program")

class TrainingEnrollments(Base):
    __tablename__ = "training_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    program_id = Column(Integer, ForeignKey("training_programs.id"))
    
    enrollment_date = Column(Date, nullable=False)
    completion_date = Column(Date)
    status = Column(String(20), default="enrolled")  # enrolled, completed, cancelled
    score = Column(Integer)  # If there's an assessment
    certificate_url = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    program = relationship("TrainingPrograms", back_populates="enrollments")

# Expense Management
class ExpenseCategories(Base):
    __tablename__ = "expense_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    expenses = relationship("Expenses", back_populates="category")

class Expenses(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    category_id = Column(Integer, ForeignKey("expense_categories.id"))
    
    title = Column(String(200), nullable=False)
    description = Column(Text)
    amount = Column(Decimal(10, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    
    receipt_url = Column(String(500))
    status = Column(String(20), default="pending")  # pending, approved, rejected, paid
    
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    approval_date = Column(Date)
    approval_comments = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees")
    category = relationship("ExpenseCategories", back_populates="expenses")
    approved_by = relationship("Users")

# Communication & Notifications
class Notifications(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50))  # info, warning, success, error
    
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    
    # Optional related entity
    related_entity_type = Column(String(50))  # lead, deal, employee, etc.
    related_entity_id = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

# Sales Targets
class SalesTargets(Base):
    __tablename__ = "sales_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    target_period = Column(String(20))  # monthly, quarterly, yearly
    target_year = Column(Integer, nullable=False)
    target_month = Column(Integer)  # For monthly targets
    target_quarter = Column(Integer)  # For quarterly targets
    
    target_amount = Column(Decimal(12, 2), nullable=False)
    achieved_amount = Column(Decimal(12, 2), default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("Users")

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
