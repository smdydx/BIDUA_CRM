
from sqlalchemy import create_engine
from models import Base
import os

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL environment variable not set!")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)

# Create all tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
