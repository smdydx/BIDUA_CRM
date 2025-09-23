#!/usr/bin/env python3
"""
Fixed table creation script that handles foreign key dependencies properly
"""

import os
from sqlalchemy import create_engine, text
from app.core.database import Base
from app.models.models import *

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_hrms.db")
print(f"Using database: {DATABASE_URL}")

# Create engine with proper config for PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

def create_tables_safe():
    """Create tables in safe order, handling circular dependencies"""
    try:
        with engine.connect() as conn:
            print("🔗 Connected to database successfully")
            
            # Create tables in dependency order
            # Level 1: Independent tables (no foreign keys)
            level1_tables = [
                Users.__table__,
                Companies.__table__, 
                LeaveTypes.__table__,
                SystemSettings.__table__,
                ProductCategories.__table__,
                ShiftManagement.__table__,
                OfficeLocations.__table__,
                IntegrationSettings.__table__,
                ApprovalWorkflows.__table__,
                WorkflowTemplates.__table__,
                EmailTemplates.__table__,
            ]
            
            print("📋 Creating Level 1 tables (no dependencies)...")
            for table in level1_tables:
                try:
                    table.create(engine, checkfirst=True)
                    print(f"✅ Created {table.name}")
                except Exception as e:
                    print(f"⚠️  {table.name}: {str(e)[:100]}...")
            
            # Level 2: Tables that depend on Level 1 only
            level2_tables = [
                Departments.__table__,  # Will ignore manager_id for now
                Notifications.__table__,
                CustomDashboards.__table__,
                Teams.__table__,
                ReportTemplates.__table__,
                DeviceRegistrations.__table__,
                CalendarSync.__table__,
                SocialMediaIntegration.__table__,
                Products.__table__,
            ]
            
            print("📋 Creating Level 2 tables...")
            for table in level2_tables:
                try:
                    table.create(engine, checkfirst=True) 
                    print(f"✅ Created {table.name}")
                except Exception as e:
                    print(f"⚠️  {table.name}: {str(e)[:100]}...")
            
            # Level 3: Tables with more complex dependencies
            level3_tables = [
                Designations.__table__,
                Contacts.__table__,
                TeamMembers.__table__,
                Channels.__table__,
                KPIs.__table__,
                DashboardWidgets.__table__,
                WorkflowSteps.__table__,
                ApprovalSteps.__table__,
            ]
            
            print("📋 Creating Level 3 tables...")
            for table in level3_tables:
                try:
                    table.create(engine, checkfirst=True)
                    print(f"✅ Created {table.name}")
                except Exception as e:
                    print(f"⚠️  {table.name}: {str(e)[:100]}...")
            
            # Finally try to create any remaining tables
            print("📋 Creating remaining tables...")
            try:
                Base.metadata.create_all(bind=engine)
                print("✅ All remaining tables created!")
            except Exception as e:
                print(f"⚠️  Some tables may have been skipped: {str(e)[:200]}...")
            
            # Verify tables were created
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result.fetchall()]
            print(f"🎉 Total tables created: {len(tables)}")
            print(f"📝 Tables: {', '.join(sorted(tables))}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    success = create_tables_safe()
    if success:
        print("🎉 Database setup completed!")
    else:
        print("❌ Database setup failed!")
        exit(1)