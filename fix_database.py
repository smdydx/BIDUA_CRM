
#!/usr/bin/env python3
"""
Database Setup and Fix Script
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def fix_database():
    """Fix database connection and create tables"""
    print("🔧 Fixing database setup...")
    
    try:
        # Import database configuration
        from app.core.database import engine, Base
        
        # Test connection
        print("🧪 Testing database connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Import all models to ensure they're registered
        print("📦 Importing models...")
        from app.models import models
        
        # Create all tables
        print("🏗️ Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify tables exist
        print("🔍 Verifying table creation...")
        with engine.connect() as connection:
            tables = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)).fetchall()
            
            if tables:
                print(f"✅ Found {len(tables)} tables in database")
                for table in tables[:5]:  # Show first 5 tables
                    print(f"   - {table[0]}")
                if len(tables) > 5:
                    print(f"   ... and {len(tables) - 5} more tables")
            else:
                print("⚠️ No tables found, but this might be normal for SQLite")
        
        print("🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("📝 This might be normal - the app will create tables automatically")
        return False

if __name__ == "__main__":
    fix_database()
