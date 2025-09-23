from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn
import os

# Import database
from app.core.database import get_db, engine, Base

# Import models to ensure they're registered
from app.models.models import *

app = FastAPI(
    title="CRM + HRMS Pro API",
    description="Complete CRM and HRMS Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security
security = HTTPBearer(auto_error=False)

# Simple auth for demo
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user - simplified for demo"""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # For demo purposes, return mock user data
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@company.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "is_active": True
    }

@app.get("/")
def read_root():
    return {"message": "CRM + HRMS Pro API is running!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CRM+HRMS Pro"}

# Authentication endpoints
@app.post("/api/v1/auth/login")
async def login(login_data: dict, db: Session = Depends(get_db)):
    """Login endpoint"""
    try:
        email = login_data.get("username") or login_data.get("email")
        password = login_data.get("password")

        if not email or not password:
            raise HTTPException(
                status_code=400,
                detail="Email and password are required"
            )

        # For demo, accept these credentials
        demo_users = {
            "admin@company.com": {"password": "admin123", "role": "admin", "name": "Admin User"},
            "hr@company.com": {"password": "hr123", "role": "hr", "name": "HR Manager"},
            "employee@company.com": {"password": "emp123", "role": "employee", "name": "John Employee"},
            "sales@company.com": {"password": "sales123", "role": "sales", "name": "Sales Rep"}
        }

        if email in demo_users and demo_users[email]["password"] == password:
            user_data = demo_users[email]
            return {
                "access_token": "demo_jwt_token",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "username": email.split("@")[0],
                    "email": email,
                    "first_name": user_data["name"].split()[0],
                    "last_name": user_data["name"].split()[-1],
                    "role": user_data["role"],
                    "is_active": True
                }
            }
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )

@app.post("/api/v1/auth/register")
async def register(user_data: dict, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        # For demo, just return success
        return {
            "access_token": "demo_jwt_token",
            "token_type": "bearer",
            "user": {
                "id": 2,
                "username": user_data.get("username"),
                "email": user_data.get("email"),
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "role": user_data.get("role", "employee"),
                "is_active": True
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Analytics endpoint
@app.get("/api/v1/analytics/dashboard")
async def get_dashboard_analytics(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get dashboard analytics data"""
    try:
        # Return mock data for demo
        return {
            "total_users": 156,
            "total_employees": 89,
            "total_companies": 45,
            "total_leads": 234,
            "total_deals": 67,
            "total_projects": 23,
            "total_tasks": 156,
            "revenue_by_stage": [
                {"stage": "Prospecting", "total_value": 250000},
                {"stage": "Discovery", "total_value": 180000},
                {"stage": "Proposal", "total_value": 320000},
                {"stage": "Negotiation", "total_value": 450000},
                {"stage": "Closed Won", "total_value": 890000}
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch analytics: {str(e)}"
        )

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    # Create tables first
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

    # In development, run backend on port 8000 (React proxy will forward API calls)
    # In production, run on port 5000 and serve both API and static files
    
    # Check if we're in development (when React dev server might be running)
    is_development = os.getenv("REPLIT_DEV_DOMAIN") or True  # Assume dev mode in Replit
    
    if is_development:
        # Development mode: Backend on port 8000, React dev server on port 5000
        port = 8000
        host = "localhost"  # Backend only needs localhost in dev
        print(f"🔧 Starting FastAPI backend server in development mode on {host}:{port}")
        print("📝 Note: React dev server should run on port 5000 with proxy to this backend")
    else:
        # Production mode: Single server on port 5000
        port = 5000
        host = "0.0.0.0"
        print(f"🚀 Starting FastAPI server in production mode on {host}:{port}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )