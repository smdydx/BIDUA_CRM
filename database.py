from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# SQLite database configuration
DATABASE_URL = "sqlite:///./crm_hrms.db"

# Create engine with SQLite optimized settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=False  # Set to True for debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()