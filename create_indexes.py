
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./crm_hrms.db"
engine = create_engine(DATABASE_URL)

def create_performance_indexes():
    """Create indexes for better query performance"""
    
    indexes = [
        # User table indexes
        "CREATE INDEX IF NOT EXISTS idx_users_email_active ON users(email, is_active)",
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
        "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)",
        "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
        
        # Employee table indexes
        "CREATE INDEX IF NOT EXISTS idx_employees_user_id ON employees(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_employees_dept_status ON employees(department_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_employees_manager ON employees(manager_id)",
        "CREATE INDEX IF NOT EXISTS idx_employees_hire_date ON employees(hire_date)",
        "CREATE INDEX IF NOT EXISTS idx_employees_employee_id ON employees(employee_id)",
        
        # Company table indexes
        "CREATE INDEX IF NOT EXISTS idx_companies_name_active ON companies(name, is_active)",
        "CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies(industry)",
        "CREATE INDEX IF NOT EXISTS idx_companies_created_at ON companies(created_at)",
        
        # Contact table indexes
        "CREATE INDEX IF NOT EXISTS idx_contacts_company_id ON contacts(company_id)",
        "CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email)",
        "CREATE INDEX IF NOT EXISTS idx_contacts_primary ON contacts(is_primary)",
        
        # Lead table indexes
        "CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status)",
        "CREATE INDEX IF NOT EXISTS idx_leads_assigned_to ON leads(assigned_to_id)",
        "CREATE INDEX IF NOT EXISTS idx_leads_company_id ON leads(company_id)",
        "CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_leads_close_date ON leads(expected_close_date)",
        
        # Deal table indexes
        "CREATE INDEX IF NOT EXISTS idx_deals_stage_owner ON deals(stage, owner_id)",
        "CREATE INDEX IF NOT EXISTS idx_deals_company_stage ON deals(company_id, stage)",
        "CREATE INDEX IF NOT EXISTS idx_deals_value ON deals(value)",
        "CREATE INDEX IF NOT EXISTS idx_deals_close_date ON deals(expected_close_date)",
        "CREATE INDEX IF NOT EXISTS idx_deals_created_at ON deals(created_at)",
        
        # Activity table indexes
        "CREATE INDEX IF NOT EXISTS idx_activities_lead_id ON activities(lead_id)",
        "CREATE INDEX IF NOT EXISTS idx_activities_deal_id ON activities(deal_id)",
        "CREATE INDEX IF NOT EXISTS idx_activities_assigned_to ON activities(assigned_to_id)",
        "CREATE INDEX IF NOT EXISTS idx_activities_scheduled ON activities(scheduled_at)",
        "CREATE INDEX IF NOT EXISTS idx_activities_completed ON activities(is_completed)",
        
        # Project table indexes
        "CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)",
        "CREATE INDEX IF NOT EXISTS idx_projects_manager ON projects(manager_id)",
        "CREATE INDEX IF NOT EXISTS idx_projects_company ON projects(company_id)",
        "CREATE INDEX IF NOT EXISTS idx_projects_dates ON projects(start_date, end_date)",
        
        # Task table indexes
        "CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to_id)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)",
        
        # Leave request indexes
        "CREATE INDEX IF NOT EXISTS idx_leave_requests_employee_status ON leave_requests(employee_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_leave_requests_dates ON leave_requests(start_date, end_date)",
        
        # Department and designation indexes
        "CREATE INDEX IF NOT EXISTS idx_departments_active ON departments(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_designations_dept ON designations(department_id)",
        
        # Attendance indexes
        "CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance(employee_id, date)",
        "CREATE INDEX IF NOT EXISTS idx_attendance_status ON attendance(status)",
        
        # Performance monitoring indexes
        "CREATE INDEX IF NOT EXISTS idx_audit_log_user_table ON audit_log(user_id, table_name)",
        "CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit_log(created_at)",
        
        # Search optimization indexes
        "CREATE INDEX IF NOT EXISTS idx_companies_name_search ON companies(name COLLATE NOCASE)",
        "CREATE INDEX IF NOT EXISTS idx_contacts_name_search ON contacts(first_name COLLATE NOCASE, last_name COLLATE NOCASE)",
        "CREATE INDEX IF NOT EXISTS idx_users_name_search ON users(first_name COLLATE NOCASE, last_name COLLATE NOCASE)",
    ]
    
    with engine.connect() as conn:
        for index_sql in indexes:
            try:
                conn.execute(text(index_sql))
                logger.info(f"✅ Created index: {index_sql.split('ON')[1].split('(')[0].strip()}")
            except Exception as e:
                logger.error(f"❌ Failed to create index: {e}")
        
        conn.commit()
    
    logger.info("🎉 Database indexing completed!")

if __name__ == "__main__":
    create_performance_indexes()
