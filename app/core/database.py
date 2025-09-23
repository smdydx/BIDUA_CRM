
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import os

Base = declarative_base()

# Database configuration - PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Development fallback to SQLite
    DATABASE_URL = "sqlite:///./crm_hrms.db"
    print("⚠️ Using SQLite for development. Set DATABASE_URL for production PostgreSQL.")
else:
    print(f"✅ Using PostgreSQL database from DATABASE_URL")

# Log database type without exposing credentials
if DATABASE_URL.startswith("postgresql://"):
    print("🗄️ Using database: PostgreSQL")
elif DATABASE_URL.startswith("sqlite://"):
    print("🗄️ Using database: SQLite")
else:
    print("🗄️ Using database: Unknown type")

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
