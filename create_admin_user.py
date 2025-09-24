#!/usr/bin/env python3
"""
Create initial admin user for the CRM+HRMS system
"""
import sys
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.database import SessionLocal, engine
from app.models.models import Users, UserRole, Base

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_admin_user():
    """Create initial admin user"""
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)

        db: Session = SessionLocal()

        # Check if admin user already exists
        existing_admin = db.query(Users).filter(Users.email == "admin@company.com").first()
        if existing_admin:
            print("✅ Admin user already exists!")
            return

        # Create admin user
        admin_user = Users(
            username="admin",
            email="admin@company.com",
            password_hash=get_password_hash("admin123"),
            first_name="System",
            last_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("✅ Admin user created successfully!")
        print("📧 Email: admin@company.com")
        print("🔑 Password: admin123")
        print("⚠️  Please change the password after first login!")

        # Create HR user
        hr_user = Users(
            username="hr_manager",
            email="hr@company.com",
            password_hash=get_password_hash("hr123"),
            first_name="HR",
            last_name="Manager",
            role=UserRole.HR,
            is_active=True
        )

        db.add(hr_user)
        db.commit()

        print("✅ HR user created successfully!")
        print("📧 Email: hr@company.com")
        print("🔑 Password: hr123")

        # Create employee user
        employee_user = Users(
            username="employee",
            email="employee@company.com",
            password_hash=get_password_hash("emp123"),
            first_name="John",
            last_name="Employee",
            role=UserRole.EMPLOYEE,
            is_active=True
        )

        db.add(employee_user)
        db.commit()

        print("✅ Employee user created successfully!")
        print("📧 Email: employee@company.com")
        print("🔑 Password: emp123")

        db.close()

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_admin_user()