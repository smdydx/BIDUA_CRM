
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import os

Base = declarative_base()

# SQLite database configuration with optimizations
DATABASE_URL = "sqlite:///./crm_hrms.db"

# Create engine with performance optimizations
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# SQLite performance optimizations
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite PRAGMA settings for performance"""
    cursor = dbapi_connection.cursor()
    
    # Performance optimizations
    cursor.execute("PRAGMA journal_mode=WAL")          # Write-Ahead Logging
    cursor.execute("PRAGMA synchronous=NORMAL")        # Faster writes
    cursor.execute("PRAGMA cache_size=10000")          # Larger cache
    cursor.execute("PRAGMA temp_store=MEMORY")         # Use memory for temp
    cursor.execute("PRAGMA mmap_size=268435456")       # Memory mapping 256MB
    cursor.execute("PRAGMA page_size=4096")            # Optimal page size
    cursor.execute("PRAGMA auto_vacuum=INCREMENTAL")   # Incremental vacuum
    cursor.execute("PRAGMA optimize")                  # Query optimization
    
    cursor.close()

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
