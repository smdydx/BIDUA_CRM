
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Time, Enum, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.sql.sqltypes import Numeric
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
    CANCELLED = "cancelled"

class ProjectStatus(enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
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
    salary = Column(Numeric(10, 2))
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
    annual_revenue = Column(Numeric(15, 2))
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
    estimated_value = Column(Numeric(12, 2))
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
    value = Column(Numeric(12, 2), nullable=False)
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
    total_hours = Column(Numeric(4, 2))
    
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
    basic_salary = Column(Numeric(10, 2), nullable=False)
    allowances = Column(Numeric(10, 2), default=0)
    overtime_amount = Column(Numeric(10, 2), default=0)
    bonus = Column(Numeric(10, 2), default=0)
    
    # Deductions
    tax_deduction = Column(Numeric(10, 2), default=0)
    insurance_deduction = Column(Numeric(10, 2), default=0)
    other_deductions = Column(Numeric(10, 2), default=0)
    
    # Totals
    gross_pay = Column(Numeric(10, 2), nullable=False)
    net_pay = Column(Numeric(10, 2), nullable=False)
    
    status = Column(Enum(PayrollStatus), default=PayrollStatus.DRAFT)
    processed_by_id = Column(Integer, ForeignKey("users.id"))
    processed_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees", back_populates="payroll_records")
    processed_by = relationship("Users")

# Customer Support & Ticketing
class SupportTickets(Base):
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(20), unique=True, nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Related entities
    customer_id = Column(Integer, ForeignKey("contacts.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # Assignment and status
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    status = Column(String(20), default="open")  # open, in_progress, resolved, closed
    category = Column(String(50))  # technical, billing, general, etc.
    
    # Resolution
    resolution = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    satisfaction_rating = Column(Integer)  # 1-5 rating
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Contacts")
    company = relationship("Companies")
    assigned_to = relationship("Users")

class TicketComments(Base):
    __tablename__ = "ticket_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Internal notes not visible to customer
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ticket = relationship("SupportTickets")
    user = relationship("Users")

# Inventory Management
class ProductCategories(Base):
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("product_categories.id"))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Self-referential relationship
    parent = relationship("ProductCategories", remote_side=[id])

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    
    # Pricing
    cost_price = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0)
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    minimum_stock_level = Column(Integer, default=10)
    unit_of_measure = Column(String(20), default="piece")
    
    # Details
    brand = Column(String(100))
    model = Column(String(100))
    barcode = Column(String(50))
    weight = Column(Numeric(8, 3))
    dimensions = Column(String(100))  # LxWxH format
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("ProductCategories")

# Financial Management
class Invoices(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    
    # Invoice details
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Amounts
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)
    paid_amount = Column(Numeric(12, 2), default=0)
    
    # Status and terms
    status = Column(String(20), default="draft")  # draft, sent, paid, overdue, cancelled
    payment_terms = Column(String(100))
    notes = Column(Text)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Companies")
    contact = relationship("Contacts")
    deal = relationship("Deals")
    created_by = relationship("Users")

class InvoiceItems(Base):
    __tablename__ = "invoice_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    description = Column(String(500), nullable=False)
    quantity = Column(Numeric(10, 3), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    
    # Relationships
    invoice = relationship("Invoices")
    product = relationship("Products")

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
    budget = Column(Numeric(12, 2))
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
    
    # Assignment
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Scheduling
    start_date = Column(Date)
    due_date = Column(Date)
    estimated_hours = Column(Numeric(5, 2))
    actual_hours = Column(Numeric(5, 2))
    
    # Status and priority
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    completion_percentage = Column(Integer, default=0)
    
    # Dependencies
    parent_task_id = Column(Integer, ForeignKey("tasks.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Projects", back_populates="tasks")
    assigned_to = relationship("Users", foreign_keys=[assigned_to_id])
    created_by = relationship("Users", foreign_keys=[created_by_id])
    parent_task = relationship("Tasks", remote_side=[id])
    subtasks = relationship("Tasks", back_populates="parent_task")


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
    cost_per_participant = Column(Numeric(10, 2))
    
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
    amount = Column(Numeric(10, 2), nullable=False)
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
    
    target_amount = Column(Numeric(12, 2), nullable=False)
    achieved_amount = Column(Numeric(12, 2), default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("Users")

# Marketing & Campaigns
class EmailTemplates(Base):
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    template_type = Column(String(50))  # welcome, follow_up, promotion, etc.
    is_active = Column(Boolean, default=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by = relationship("Users")

class EmailCampaigns(Base):
    __tablename__ = "email_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"))
    
    # Campaign settings
    subject = Column(String(200), nullable=False)
    sender_name = Column(String(100))
    sender_email = Column(String(100))
    
    # Scheduling
    status = Column(String(20), default="draft")  # draft, scheduled, sending, sent, paused
    scheduled_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True))
    
    # Statistics
    total_recipients = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    emails_delivered = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    emails_clicked = Column(Integer, default=0)
    emails_bounced = Column(Integer, default=0)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    template = relationship("EmailTemplates")
    created_by = relationship("Users")

class CampaignRecipients(Base):
    __tablename__ = "campaign_recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    
    # Tracking
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    opened_at = Column(DateTime(timezone=True))
    clicked_at = Column(DateTime(timezone=True))
    bounced_at = Column(DateTime(timezone=True))
    unsubscribed_at = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String(20), default="pending")  # pending, sent, delivered, opened, clicked, bounced
    
    # Relationships
    campaign = relationship("EmailCampaigns")
    contact = relationship("Contacts")



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

# ============================================================================
# ADVANCED SECURITY & ACCESS CONTROL
# ============================================================================

class Permissions(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    module = Column(String(50), nullable=False)  # CRM, HR, Project, etc.
    action = Column(String(50), nullable=False)  # create, read, update, delete, export
    resource = Column(String(50), nullable=False)  # leads, employees, projects
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RolePermissions(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRole), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    is_granted = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permission = relationship("Permissions")

class UserSessions(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    location = Column(String(200))  # City, Country
    device_type = Column(String(50))  # Desktop, Mobile, Tablet
    browser = Column(String(100))
    
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class TwoFactorAuth(Base):
    __tablename__ = "two_factor_auth"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    secret_key = Column(String(255), nullable=False)
    is_enabled = Column(Boolean, default=False)
    backup_codes = Column(Text)  # JSON array of backup codes
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("Users")

class IPRestrictions(Base):
    __tablename__ = "ip_restrictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45), nullable=False)
    ip_range = Column(String(100))  # CIDR notation for ranges
    description = Column(String(200))
    is_allowed = Column(Boolean, default=True)  # True=whitelist, False=blacklist
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class PasswordPolicies(Base):
    __tablename__ = "password_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    min_length = Column(Integer, default=8)
    require_uppercase = Column(Boolean, default=True)
    require_lowercase = Column(Boolean, default=True)
    require_numbers = Column(Boolean, default=True)
    require_special_chars = Column(Boolean, default=True)
    max_age_days = Column(Integer, default=90)  # Password expiry
    history_count = Column(Integer, default=5)  # Prevent reuse of last N passwords
    max_failed_attempts = Column(Integer, default=5)
    lockout_duration_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PasswordHistory(Base):
    __tablename__ = "password_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    password_hash = Column(String(255), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class LoginAttempts(Base):
    __tablename__ = "login_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    is_successful = Column(Boolean, default=False)
    failure_reason = Column(String(100))  # invalid_password, account_locked, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

# ============================================================================
# INTERNAL COMMUNICATION SYSTEM
# ============================================================================

class Teams(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    team_type = Column(String(50), default="department")  # department, project, temporary
    is_public = Column(Boolean, default=True)  # Public teams anyone can join
    max_members = Column(Integer)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_by = relationship("Users")

class TeamMembers(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), default="member")  # admin, moderator, member
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('team_id', 'user_id', name='unique_team_member'),
    )
    
    # Relationships
    team = relationship("Teams")
    user = relationship("Users")

class Channels(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    team_id = Column(Integer, ForeignKey("teams.id"))
    channel_type = Column(String(20), default="public")  # public, private, direct
    is_archived = Column(Boolean, default=False)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    team = relationship("Teams")
    created_by = relationship("Users")

class Messages(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    parent_message_id = Column(Integer, ForeignKey("messages.id"))  # For threaded replies
    
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, file, image, system
    
    # File attachments
    file_url = Column(String(500))
    file_name = Column(String(255))
    file_size = Column(Integer)
    
    # Message status
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    edited_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    channel = relationship("Channels")
    sender = relationship("Users")
    parent_message = relationship("Messages", remote_side=[id])

class MessageReactions(Base):
    __tablename__ = "message_reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    emoji = Column(String(10), nullable=False)  # 👍, ❤️, 😄, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('message_id', 'user_id', 'emoji', name='unique_message_reaction'),
    )
    
    # Relationships
    message = relationship("Messages")
    user = relationship("Users")

class DirectMessages(Base):
    __tablename__ = "direct_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    
    # File attachments
    file_url = Column(String(500))
    file_name = Column(String(255))
    
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sender = relationship("Users", foreign_keys=[sender_id])
    recipient = relationship("Users", foreign_keys=[recipient_id])

class VideoMeetings(Base):
    __tablename__ = "video_meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    meeting_url = Column(String(500))
    meeting_id = Column(String(100))
    password = Column(String(50))
    
    # Scheduling
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    scheduled_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))
    
    # Settings
    max_participants = Column(Integer, default=50)
    is_recording_enabled = Column(Boolean, default=False)
    waiting_room_enabled = Column(Boolean, default=True)
    
    # Status
    status = Column(String(20), default="scheduled")  # scheduled, in_progress, ended, cancelled
    
    host_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    host = relationship("Users")

class MeetingParticipants(Base):
    __tablename__ = "meeting_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("video_meetings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    joined_at = Column(DateTime(timezone=True))
    left_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    meeting = relationship("VideoMeetings")
    user = relationship("Users")

class Announcements(Base):
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    announcement_type = Column(String(50), default="general")  # general, urgent, policy, event
    
    # Targeting
    target_audience = Column(String(50), default="all")  # all, department, role, team
    target_department_id = Column(Integer, ForeignKey("departments.id"))
    target_role = Column(Enum(UserRole))
    target_team_id = Column(Integer, ForeignKey("teams.id"))
    
    # Settings
    is_pinned = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True))
    requires_acknowledgment = Column(Boolean, default=False)
    
    # Status
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_by = relationship("Users")
    target_department = relationship("Departments")
    target_team = relationship("Teams")

class AnnouncementAcknowledgments(Base):
    __tablename__ = "announcement_acknowledgments"
    
    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    acknowledged_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('announcement_id', 'user_id', name='unique_announcement_ack'),
    )
    
    # Relationships
    announcement = relationship("Announcements")
    user = relationship("Users")

# ============================================================================
# WORKFLOW AUTOMATION
# ============================================================================

class WorkflowTemplates(Base):
    __tablename__ = "workflow_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # HR, CRM, Project, Finance
    trigger_type = Column(String(50), nullable=False)  # manual, scheduled, event_based
    trigger_config = Column(Text)  # JSON configuration for triggers
    
    is_active = Column(Boolean, default=True)
    is_system_template = Column(Boolean, default=False)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_by = relationship("Users")

class WorkflowSteps(Base):
    __tablename__ = "workflow_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_template_id = Column(Integer, ForeignKey("workflow_templates.id"))
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(200), nullable=False)
    step_type = Column(String(50), nullable=False)  # approval, email, task_create, data_update
    step_config = Column(Text, nullable=False)  # JSON configuration
    
    # Conditions
    condition_type = Column(String(50), default="always")  # always, conditional
    condition_config = Column(Text)  # JSON condition configuration
    
    # Error handling
    on_error = Column(String(50), default="stop")  # stop, continue, retry
    retry_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow_template = relationship("WorkflowTemplates")

class WorkflowInstances(Base):
    __tablename__ = "workflow_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_template_id = Column(Integer, ForeignKey("workflow_templates.id"))
    triggered_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Context
    entity_type = Column(String(50))  # lead, employee, deal, etc.
    entity_id = Column(Integer)
    context_data = Column(Text)  # JSON data for workflow context
    
    # Status
    status = Column(String(20), default="running")  # running, completed, failed, cancelled
    current_step = Column(Integer, default=1)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    workflow_template = relationship("WorkflowTemplates")
    triggered_by = relationship("Users")

class WorkflowExecutions(Base):
    __tablename__ = "workflow_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_instance_id = Column(Integer, ForeignKey("workflow_instances.id"))
    step_id = Column(Integer, ForeignKey("workflow_steps.id"))
    
    # Execution details
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    input_data = Column(Text)  # JSON input data
    output_data = Column(Text)  # JSON output data
    error_message = Column(Text)
    
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    workflow_instance = relationship("WorkflowInstances")
    step = relationship("WorkflowSteps")

class ApprovalWorkflows(Base):
    __tablename__ = "approval_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    entity_type = Column(String(50), nullable=False)  # leave_request, expense, deal
    
    # Approval chain configuration
    approval_levels = Column(Integer, default=1)
    is_sequential = Column(Boolean, default=True)  # Sequential vs parallel approval
    require_all_approvers = Column(Boolean, default=True)
    
    # Auto-approval conditions
    auto_approval_conditions = Column(Text)  # JSON conditions for auto-approval
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ApprovalSteps(Base):
    __tablename__ = "approval_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("approval_workflows.id"))
    step_level = Column(Integer, nullable=False)
    approver_type = Column(String(50), nullable=False)  # user, role, manager, department_head
    approver_id = Column(Integer, ForeignKey("users.id"))
    approver_role = Column(Enum(UserRole))
    
    # Conditions
    conditions = Column(Text)  # JSON conditions when this step applies
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow = relationship("ApprovalWorkflows")
    approver = relationship("Users")

class ApprovalRequests(Base):
    __tablename__ = "approval_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("approval_workflows.id"))
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    
    requested_by_id = Column(Integer, ForeignKey("users.id"))
    current_step = Column(Integer, default=1)
    status = Column(String(20), default="pending")  # pending, approved, rejected, cancelled
    
    # Request data
    request_data = Column(Text)  # JSON data of the request
    justification = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    workflow = relationship("ApprovalWorkflows")
    requested_by = relationship("Users")

class ApprovalActions(Base):
    __tablename__ = "approval_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    approval_request_id = Column(Integer, ForeignKey("approval_requests.id"))
    step_level = Column(Integer, nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"))
    
    action = Column(String(20), nullable=False)  # approved, rejected, delegated
    comments = Column(Text)
    delegated_to_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    approval_request = relationship("ApprovalRequests")
    approver = relationship("Users", foreign_keys=[approver_id])
    delegated_to = relationship("Users", foreign_keys=[delegated_to_id])

class EmailAutomation(Base):
    __tablename__ = "email_automation"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    trigger_event = Column(String(100), nullable=False)  # lead_created, deal_won, employee_joined
    
    # Email settings
    template_id = Column(Integer, ForeignKey("email_templates.id"))
    sender_email = Column(String(100))
    sender_name = Column(String(100))
    
    # Trigger conditions
    conditions = Column(Text)  # JSON conditions
    delay_minutes = Column(Integer, default=0)  # Delay before sending
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    template = relationship("EmailTemplates")

class AutomatedEmails(Base):
    __tablename__ = "automated_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    automation_id = Column(Integer, ForeignKey("email_automation.id"))
    recipient_email = Column(String(100), nullable=False)
    recipient_name = Column(String(100))
    
    # Trigger context
    trigger_entity_type = Column(String(50))
    trigger_entity_id = Column(Integer)
    
    # Email content (after template processing)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    
    # Status
    status = Column(String(20), default="queued")  # queued, sent, failed, cancelled
    sent_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    automation = relationship("EmailAutomation")

# ============================================================================
# ADVANCED ANALYTICS & REPORTING
# ============================================================================

class CustomDashboards(Base):
    __tablename__ = "custom_dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    layout_config = Column(Text, nullable=False)  # JSON layout configuration
    
    # Access control
    created_by_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    allowed_roles = Column(Text)  # JSON array of allowed roles
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by = relationship("Users")

class DashboardWidgets(Base):
    __tablename__ = "dashboard_widgets"
    
    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, ForeignKey("custom_dashboards.id"))
    widget_type = Column(String(50), nullable=False)  # chart, table, metric, progress
    widget_title = Column(String(200), nullable=False)
    
    # Position and size
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=1)
    height = Column(Integer, default=1)
    
    # Widget configuration
    data_source = Column(String(100), nullable=False)  # Table or view name
    query_config = Column(Text, nullable=False)  # JSON query configuration
    chart_config = Column(Text)  # JSON chart styling configuration
    refresh_interval = Column(Integer, default=300)  # Refresh interval in seconds
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    dashboard = relationship("CustomDashboards")

class KPIs(Base):
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # sales, hr, finance, project
    
    # KPI calculation
    calculation_method = Column(String(50), nullable=False)  # sum, average, count, percentage
    data_source = Column(String(100), nullable=False)
    calculation_config = Column(Text, nullable=False)  # JSON calculation configuration
    
    # Target and thresholds
    target_value = Column(Numeric(15, 2))
    warning_threshold = Column(Numeric(15, 2))
    critical_threshold = Column(Numeric(15, 2))
    
    # Display settings
    unit = Column(String(20))  # %, $, units, etc.
    decimal_places = Column(Integer, default=2)
    
    is_active = Column(Boolean, default=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_by = relationship("Users")

class KPIValues(Base):
    __tablename__ = "kpi_values"
    
    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id"))
    
    # Time period
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly, yearly
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Values
    actual_value = Column(Numeric(15, 2), nullable=False)
    target_value = Column(Numeric(15, 2))
    previous_value = Column(Numeric(15, 2))  # For comparison
    
    # Calculated metrics
    variance_amount = Column(Numeric(15, 2))
    variance_percentage = Column(Numeric(5, 2))
    trend = Column(String(20))  # up, down, stable
    
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    kpi = relationship("KPIs")

class ReportTemplates(Base):
    __tablename__ = "report_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # sales, hr, finance, custom
    
    # Report configuration
    data_sources = Column(Text, nullable=False)  # JSON array of tables/views
    query_config = Column(Text, nullable=False)  # JSON query configuration
    filters_config = Column(Text)  # JSON available filters configuration
    
    # Output settings
    output_format = Column(String(20), default="pdf")  # pdf, excel, csv
    page_orientation = Column(String(20), default="portrait")  # portrait, landscape
    include_charts = Column(Boolean, default=True)
    
    # Access control
    created_by_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    allowed_roles = Column(Text)  # JSON array of allowed roles
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_by = relationship("Users")

class GeneratedReports(Base):
    __tablename__ = "generated_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("report_templates.id"))
    report_name = Column(String(200), nullable=False)
    
    # Generation details
    generated_by_id = Column(Integer, ForeignKey("users.id"))
    filter_params = Column(Text)  # JSON parameters used for generation
    
    # File details
    file_path = Column(String(500))
    file_size = Column(Integer)
    file_format = Column(String(20))
    
    # Status
    status = Column(String(20), default="generating")  # generating, completed, failed
    error_message = Column(Text)
    
    # Analytics
    download_count = Column(Integer, default=0)
    last_downloaded = Column(DateTime(timezone=True))
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # Auto-delete after expiry
    
    # Relationships
    template = relationship("ReportTemplates")
    generated_by = relationship("Users")

class DataExports(Base):
    __tablename__ = "data_exports"
    
    id = Column(Integer, primary_key=True, index=True)
    export_name = Column(String(200), nullable=False)
    entity_type = Column(String(50), nullable=False)  # leads, employees, deals, etc.
    
    # Export configuration
    columns = Column(Text, nullable=False)  # JSON array of columns to export
    filters = Column(Text)  # JSON filters applied
    export_format = Column(String(20), default="csv")  # csv, excel, json
    
    # File details
    file_path = Column(String(500))
    file_size = Column(Integer)
    record_count = Column(Integer)
    
    # Status
    status = Column(String(20), default="processing")  # processing, completed, failed
    progress_percentage = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Request details
    requested_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    requested_by = relationship("Users")

# ============================================================================
# THIRD-PARTY INTEGRATIONS
# ============================================================================

class IntegrationSettings(Base):
    __tablename__ = "integration_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    integration_name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # communication, payment, calendar, social
    
    # Configuration
    config_schema = Column(Text, nullable=False)  # JSON schema for configuration
    current_config = Column(Text)  # JSON current configuration values
    
    # Status
    is_enabled = Column(Boolean, default=False)
    is_configured = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True))
    sync_status = Column(String(20))  # success, error, in_progress
    
    # API details
    api_version = Column(String(20))
    webhook_url = Column(String(500))
    webhook_secret = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WebhookLogs(Base):
    __tablename__ = "webhook_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    integration_name = Column(String(100), nullable=False)
    webhook_event = Column(String(100), nullable=False)
    
    # Request details
    request_headers = Column(Text)  # JSON headers
    request_body = Column(Text)  # JSON body
    source_ip = Column(String(45))
    
    # Response details
    response_status = Column(Integer)
    response_body = Column(Text)
    processing_time_ms = Column(Integer)
    
    # Status
    is_processed = Column(Boolean, default=False)
    error_message = Column(Text)
    
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Index for performance
    __table_args__ = (
        Index('idx_webhook_logs_integration_event', 'integration_name', 'webhook_event'),
    )

class CalendarSync(Base):
    __tablename__ = "calendar_sync"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    calendar_provider = Column(String(50), nullable=False)  # google, outlook, apple
    
    # Authentication
    access_token = Column(String(1000))
    refresh_token = Column(String(1000))
    expires_at = Column(DateTime(timezone=True))
    
    # Calendar details
    external_calendar_id = Column(String(200))
    calendar_name = Column(String(200))
    
    # Sync settings
    is_bidirectional = Column(Boolean, default=True)
    sync_meetings = Column(Boolean, default=True)
    sync_tasks = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class SocialMediaIntegration(Base):
    __tablename__ = "social_media_integration"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)  # linkedin, twitter, facebook
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Authentication
    access_token = Column(String(1000))
    refresh_token = Column(String(1000))
    expires_at = Column(DateTime(timezone=True))
    
    # Profile information
    external_user_id = Column(String(200))
    username = Column(String(100))
    profile_url = Column(String(500))
    
    # Sync settings
    auto_post_achievements = Column(Boolean, default=False)
    sync_contacts = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class PaymentGatewaySettings(Base):
    __tablename__ = "payment_gateway_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    gateway_name = Column(String(50), unique=True, nullable=False)  # razorpay, stripe, paypal
    display_name = Column(String(100), nullable=False)
    
    # API Configuration
    api_key = Column(String(500))
    api_secret = Column(String(500))
    webhook_secret = Column(String(255))
    sandbox_mode = Column(Boolean, default=True)
    
    # Gateway settings
    supported_currencies = Column(Text)  # JSON array of supported currencies
    default_currency = Column(String(10), default="INR")
    
    # Features
    supports_subscriptions = Column(Boolean, default=False)
    supports_refunds = Column(Boolean, default=True)
    supports_webhooks = Column(Boolean, default=True)
    
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PaymentTransactions(Base):
    __tablename__ = "payment_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, nullable=False)
    gateway_name = Column(String(50), nullable=False)
    gateway_transaction_id = Column(String(200))
    
    # Transaction details
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    transaction_type = Column(String(50), nullable=False)  # payment, refund, subscription
    
    # Related entities
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    customer_id = Column(Integer, ForeignKey("contacts.id"))
    
    # Status
    status = Column(String(20), default="pending")  # pending, success, failed, cancelled
    failure_reason = Column(String(200))
    
    # Gateway response
    gateway_response = Column(Text)  # JSON gateway response
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    invoice = relationship("Invoices")
    customer = relationship("Contacts")

# ============================================================================
# MOBILE APP SUPPORT
# ============================================================================

class DeviceRegistrations(Base):
    __tablename__ = "device_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_token = Column(String(500), unique=True, nullable=False)
    device_type = Column(String(20), nullable=False)  # ios, android
    device_model = Column(String(100))
    app_version = Column(String(20))
    os_version = Column(String(20))
    
    # Settings
    push_notifications_enabled = Column(Boolean, default=True)
    notification_preferences = Column(Text)  # JSON preferences
    
    is_active = Column(Boolean, default=True)
    last_active = Column(DateTime(timezone=True))
    
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class PushNotifications(Base):
    __tablename__ = "push_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_token = Column(String(500))
    
    # Notification content
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String(50))  # message, reminder, alert, update
    
    # Payload
    data_payload = Column(Text)  # JSON additional data
    action_url = Column(String(500))  # Deep link for action
    
    # Related entity
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    
    # Status
    status = Column(String(20), default="queued")  # queued, sent, delivered, failed
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Analytics
    is_clicked = Column(Boolean, default=False)
    clicked_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class MobileAPILogs(Base):
    __tablename__ = "mobile_api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_token = Column(String(500))
    
    # Request details
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    request_headers = Column(Text)
    request_body = Column(Text)
    
    # Response details
    response_status = Column(Integer)
    response_size = Column(Integer)
    response_time_ms = Column(Integer)
    
    # Device info
    app_version = Column(String(20))
    device_model = Column(String(100))
    os_version = Column(String(20))
    network_type = Column(String(20))  # wifi, cellular, unknown
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("Users")

class OfflineSync(Base):
    __tablename__ = "offline_sync"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_token = Column(String(500))
    
    # Sync details
    entity_type = Column(String(50), nullable=False)  # contacts, tasks, attendance
    entity_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # create, update, delete
    
    # Data
    sync_data = Column(Text, nullable=False)  # JSON data to sync
    conflict_resolution = Column(String(20), default="server_wins")  # server_wins, client_wins, manual
    
    # Status
    status = Column(String(20), default="pending")  # pending, synced, conflict, failed
    error_message = Column(Text)
    
    # Timestamps
    client_timestamp = Column(DateTime(timezone=True), nullable=False)
    server_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    synced_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("Users")

class GPSAttendance(Base):
    __tablename__ = "gps_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    attendance_id = Column(Integer, ForeignKey("attendance.id"))
    
    # GPS location
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    accuracy_meters = Column(Numeric(8, 2))
    address = Column(String(500))
    
    # Verification
    is_within_geofence = Column(Boolean, default=False)
    distance_from_office_meters = Column(Integer)
    office_location_id = Column(Integer, ForeignKey("office_locations.id"))
    
    # Device info
    device_info = Column(Text)  # JSON device information
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    attendance = relationship("Attendance")

class OfficeLocations(Base):
    __tablename__ = "office_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    
    # GPS coordinates
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    
    # Geofence settings
    geofence_radius_meters = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    
    # Working hours
    working_hours_config = Column(Text)  # JSON working hours for this location
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ============================================================================
# ADVANCED HR FEATURES
# ============================================================================

class JobPostings(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    
    # Job details
    employment_type = Column(String(20), default="Full-time")  # Full-time, Part-time, Contract
    experience_required = Column(String(50))  # 0-1 years, 2-5 years, etc.
    salary_range_min = Column(Numeric(10, 2))
    salary_range_max = Column(Numeric(10, 2))
    
    # Requirements
    skills_required = Column(Text)  # JSON array of required skills
    qualifications = Column(Text)  # JSON array of qualifications
    responsibilities = Column(Text)
    benefits = Column(Text)
    
    # Application settings
    application_deadline = Column(Date)
    max_applications = Column(Integer)
    is_remote_allowed = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default="draft")  # draft, published, closed, cancelled
    published_at = Column(DateTime(timezone=True))
    
    # Posting details
    posted_by_id = Column(Integer, ForeignKey("users.id"))
    hiring_manager_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    department = relationship("Departments")
    designation = relationship("Designations")
    posted_by = relationship("Users", foreign_keys=[posted_by_id])
    hiring_manager = relationship("Users", foreign_keys=[hiring_manager_id])

class JobApplications(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"))
    
    # Applicant details
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    
    # Resume and documents
    resume_url = Column(String(500))
    cover_letter = Column(Text)
    portfolio_url = Column(String(500))
    
    # Application details
    current_salary = Column(Numeric(10, 2))
    expected_salary = Column(Numeric(10, 2))
    notice_period_days = Column(Integer)
    available_from = Column(Date)
    
    # Screening
    application_source = Column(String(50))  # website, linkedin, referral
    referrer_employee_id = Column(Integer, ForeignKey("employees.id"))
    
    # Status tracking
    status = Column(String(20), default="applied")  # applied, screening, interview, selected, rejected
    stage = Column(String(50))  # phone_screen, technical_round, hr_round, final_round
    
    # Review
    reviewer_notes = Column(Text)
    rating = Column(Integer)  # 1-5 rating
    rejection_reason = Column(String(200))
    
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    job_posting = relationship("JobPostings")
    referrer = relationship("Employees")

class InterviewSchedules(Base):
    __tablename__ = "interview_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    job_application_id = Column(Integer, ForeignKey("job_applications.id"))
    interview_round = Column(String(50), nullable=False)  # phone_screen, technical, hr, final
    
    # Scheduling
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, default=60)
    
    # Location/Method
    interview_type = Column(String(20), default="in_person")  # in_person, video, phone
    location = Column(String(200))
    meeting_link = Column(String(500))
    
    # Participants
    interviewer_id = Column(Integer, ForeignKey("users.id"))
    additional_interviewers = Column(Text)  # JSON array of user IDs
    
    # Status
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled, rescheduled
    feedback = Column(Text)
    rating = Column(Integer)  # 1-5 rating
    recommendation = Column(String(20))  # hire, reject, next_round
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_application = relationship("JobApplications")
    interviewer = relationship("Users")

class PerformanceGoals(Base):
    __tablename__ = "performance_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    goal_title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Goal details
    goal_type = Column(String(50), default="performance")  # performance, development, behavioral
    category = Column(String(50))  # sales, quality, efficiency, learning
    
    # SMART goal attributes
    specific_description = Column(Text)
    measurable_criteria = Column(Text)
    achievable_steps = Column(Text)
    relevant_reason = Column(Text)
    time_bound_deadline = Column(Date)
    
    # Targets
    target_value = Column(Numeric(12, 2))
    target_unit = Column(String(50))  # percentage, amount, count
    current_value = Column(Numeric(12, 2), default=0)
    
    # Timeline
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Status
    status = Column(String(20), default="active")  # active, completed, cancelled, overdue
    completion_percentage = Column(Integer, default=0)
    
    # Review
    assigned_by_id = Column(Integer, ForeignKey("users.id"))
    last_review_date = Column(Date)
    next_review_date = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employees")
    assigned_by = relationship("Users")

class GoalProgress(Base):
    __tablename__ = "goal_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("performance_goals.id"))
    
    # Progress details
    progress_date = Column(Date, nullable=False)
    progress_value = Column(Numeric(12, 2), nullable=False)
    progress_percentage = Column(Integer, nullable=False)
    notes = Column(Text)
    
    # Evidence
    evidence_files = Column(Text)  # JSON array of file URLs
    
    # Review
    reviewed_by_id = Column(Integer, ForeignKey("users.id"))
    review_comments = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    goal = relationship("PerformanceGoals")
    reviewed_by = relationship("Users")

class EmployeeSelfService(Base):
    __tablename__ = "employee_self_service"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    request_type = Column(String(50), nullable=False)  # personal_info, address, emergency_contact, bank_details
    
    # Request data
    current_data = Column(Text)  # JSON current data
    requested_data = Column(Text, nullable=False)  # JSON requested changes
    change_reason = Column(Text)
    
    # Supporting documents
    supporting_documents = Column(Text)  # JSON array of document URLs
    
    # Status
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reviewed_by_id = Column(Integer, ForeignKey("users.id"))
    review_date = Column(DateTime(timezone=True))
    review_comments = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    reviewed_by = relationship("Users")

class TimeTracking(Base):
    __tablename__ = "time_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    
    # Time details
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    total_minutes = Column(Integer)
    break_minutes = Column(Integer, default=0)
    
    # Description
    description = Column(Text)
    activity_type = Column(String(50))  # development, meeting, research, testing
    
    # Status
    is_billable = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    project = relationship("Projects")
    task = relationship("Tasks")
    approved_by = relationship("Users")

class ShiftManagement(Base):
    __tablename__ = "shift_management"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Shift timing
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_duration_minutes = Column(Integer, default=60)
    
    # Working days
    working_days = Column(Text, nullable=False)  # JSON array of days [1,2,3,4,5] for Mon-Fri
    
    # Settings
    grace_period_minutes = Column(Integer, default=15)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EmployeeShiftAssignment(Base):
    __tablename__ = "employee_shift_assignment"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    shift_id = Column(Integer, ForeignKey("shift_management.id"))
    
    # Assignment period
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    
    # Override settings for this employee
    custom_start_time = Column(Time)
    custom_end_time = Column(Time)
    custom_working_days = Column(Text)  # JSON array
    
    is_active = Column(Boolean, default=True)
    assigned_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employees")
    shift = relationship("ShiftManagement")
    assigned_by = relationship("Users")
