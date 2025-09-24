
#!/usr/bin/env python3
"""
Simple backend startup script for CRM+HRMS Pro
"""
import sys
import os
import uvicorn
from pathlib import Path

def main():
    print("🚀 Starting CRM+HRMS Pro Backend Server...")
    print("=" * 50)
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("❌ main.py not found!")
        sys.exit(1)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=5000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
