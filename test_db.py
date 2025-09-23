#!/usr/bin/env python3

import sys
sys.path.append('.')

from app.core.database import engine
from sqlalchemy import text

print("Testing database connection...")

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Database connection successful:', result.fetchone())
except Exception as e:
    print(f'❌ Database connection failed: {e}')