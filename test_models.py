#!/usr/bin/env python3

import sys
sys.path.append('.')

from app.core.database import engine, Base
from app.models.models import Users  # Import just one model first

print("Testing table creation...")

try:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print('✅ Tables created successfully!')
    
    # Test a simple query
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    user_count = session.query(Users).count()
    print(f'✅ Query successful! Current user count: {user_count}')
    
except Exception as e:
    print(f'❌ Table creation failed: {e}')
    import traceback
    traceback.print_exc()