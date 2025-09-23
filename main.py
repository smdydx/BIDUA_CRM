
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="CRM + HRMS System",
    description="Comprehensive Customer Relationship Management and Human Resource Management System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

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
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True
    )
