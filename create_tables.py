
from sqlalchemy import create_engine
from app.models.models import Base
import os

# Get database URL - use SQLite if DATABASE_URL not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_hrms.db")

print(f"Using database: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

# Create all tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
