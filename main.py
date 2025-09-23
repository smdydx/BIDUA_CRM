from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.core.database import get_db, engine
from app.models.models import Base
from app.middleware.middleware import add_all_middleware
import app.crud.crud as crud
import app.schemas.schemas as schemas
import uvicorn
import asyncio

# Create FastAPI app
app = FastAPI(
    title="CRM + HRMS System",
    description="Comprehensive Customer Relationship Management and Human Resource Management System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all custom middleware
add_all_middleware(app)

# Security
security = HTTPBearer(auto_error=False)

# Lifespan event handler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
    yield
    # Shutdown (if needed)
    pass

@app.get("/")
async def root():
    return {
        "message": "Welcome to CRM + HRMS System",
        "status": "active",
        "features": [
            "Customer Relationship Management",
            "Human Resource Management", 
            "Project Management",
            "Task Management",
            "Training & Development",
            "Expense Management",
            "Document Management",
            "Email Campaigns",
            "Support Ticketing",
            "Inventory Management",
            "Financial Management"
        ]
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Include routers - import from endpoints
from app.api.v1.endpoints import auth, users, hr, crm, projects, analytics

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(hr.router, prefix="/api/v1/hr", tags=["HR Management"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["CRM"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Project Management"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True
    )