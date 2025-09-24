from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - prefer SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    print("🗄️ Using PostgreSQL database")
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
else:
    print("🗄️ Using SQLite database (fallback)")
    # SQLite fallback
    DATABASE_URL = "sqlite:///./crm_hrms.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def init_database():
    """Initialize database with proper error handling"""
    try:
        # Import here to avoid circular imports
        from app.models.models import Base
        
        # Create all tables
        print("🔧 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Test basic query
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        
        return True
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
        print("📦 Tables will be created automatically when first accessed")
        return False