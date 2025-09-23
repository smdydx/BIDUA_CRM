
#!/usr/bin/env python3
"""
Create default admin user for CRM+HRMS System
"""

import hashlib
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.models.models import Users, UserRole
from datetime import datetime

def create_admin_user():
    """Create default admin user"""
    db = Session(bind=engine)
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(Users).filter(Users.email == "admin@company.com").first()
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"📧 Email: admin@company.com")
            print(f"🔑 Password: admin123")
            return
        
        # Create admin user
        admin_data = {
            "username": "admin",
            "email": "admin@company.com",
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
            "first_name": "System",
            "last_name": "Administrator", 
            "phone": "+91-9999999999",
            "role": UserRole.ADMIN,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        admin_user = Users(**admin_data)
        db.add(admin_user)
        
        # Create HR user
        hr_data = {
            "username": "hr_manager",
            "email": "hr@company.com",
            "password_hash": hashlib.sha256("hr123".encode()).hexdigest(),
            "first_name": "HR",
            "last_name": "Manager",
            "phone": "+91-8888888888",
            "role": UserRole.HR,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        hr_user = Users(**hr_data)
        db.add(hr_user)
        
        # Create Employee user
        employee_data = {
            "username": "employee",
            "email": "employee@company.com", 
            "password_hash": hashlib.sha256("emp123".encode()).hexdigest(),
            "first_name": "John",
            "last_name": "Employee",
            "phone": "+91-7777777777",
            "role": UserRole.EMPLOYEE,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        employee_user = Users(**employee_data)
        db.add(employee_user)
        
        # Create Sales user 
        sales_data = {
            "username": "sales_rep",
            "email": "sales@company.com",
            "password_hash": hashlib.sha256("sales123".encode()).hexdigest(),
            "first_name": "Sales",
            "last_name": "Representative",
            "phone": "+91-6666666666",
            "role": UserRole.SALES,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        sales_user = Users(**sales_data)
        db.add(sales_user)
        
        db.commit()
        
        print("🚀 Default users created successfully!")
        print("\n" + "="*50)
        print("📋 LOGIN CREDENTIALS:")
        print("="*50)
        print("👨‍💼 ADMIN LOGIN:")
        print("   📧 Email: admin@company.com")
        print("   🔑 Password: admin123")
        print("   🎯 Role: Administrator (Full Access)")
        print()
        print("👥 HR MANAGER LOGIN:")
        print("   📧 Email: hr@company.com") 
        print("   🔑 Password: hr123")
        print("   🎯 Role: HR Manager")
        print()
        print("👤 EMPLOYEE LOGIN:")
        print("   📧 Email: employee@company.com")
        print("   🔑 Password: emp123")
        print("   🎯 Role: Employee")
        print()
        print("💰 SALES REP LOGIN:")
        print("   📧 Email: sales@company.com")
        print("   🔑 Password: sales123")
        print("   🎯 Role: Sales Representative")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating users: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
