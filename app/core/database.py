
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import os

Base = declarative_base()

# Database configuration - SQLite for reliable operation
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_hrms.db")

print(f"🗄️ Using database: {DATABASE_URL}")

# Create engine with performance optimizations for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Create session factory with optimizations
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Keep objects usable after commit
)

# Dependency for FastAPI with caching
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connection pool monitoring
def get_db_stats():
    """Get database connection pool statistics"""
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid()
    }
