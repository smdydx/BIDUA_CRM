
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
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
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

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

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True
    )
