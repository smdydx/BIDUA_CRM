
#!/usr/bin/env python3
"""
Comprehensive issue fixer for CRM+HRMS Pro Backend
"""
import os
import sys
import subprocess
from pathlib import Path

def fix_database():
    """Fix database issues"""
    print("🔧 Fixing database...")
    try:
        subprocess.run([sys.executable, "fix_database.py"], check=True)
        print("✅ Database fixed")
        return True
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False

def create_admin():
    """Create admin user"""
    print("👤 Creating admin user...")
    try:
        subprocess.run([sys.executable, "create_admin_user.py"], check=True)
        print("✅ Admin user created")
        return True
    except Exception as e:
        print(f"❌ Admin creation failed: {e}")
        return False

def check_dependencies():
    """Check if all Python dependencies are installed"""
    print("📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import jose
        import passlib
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("📁 Checking required files...")
    required_files = [
        "main.py",
        "app/core/database.py",
        "app/models/models.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def fix_permissions():
    """Fix file permissions"""
    print("🔒 Fixing permissions...")
    try:
        scripts = ["fix_database.py", "create_admin_user.py", "main.py"]
        for script in scripts:
            if Path(script).exists():
                os.chmod(script, 0o755)
        print("✅ Permissions fixed")
        return True
    except Exception as e:
        print(f"❌ Permission fix failed: {e}")
        return False

def main():
    print("🔧 CRM+HRMS Pro Backend Issue Fixer")
    print("=" * 50)
    
    issues_found = 0
    issues_fixed = 0
    
    # Check files
    if not check_files():
        issues_found += 1
        print("⚠️ Some required files are missing")
    else:
        issues_fixed += 1
    
    # Check dependencies
    if not check_dependencies():
        issues_found += 1
        print("⚠️ Installing missing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            issues_fixed += 1
        except:
            print("❌ Failed to install dependencies")
    else:
        issues_fixed += 1
    
    # Fix permissions
    if fix_permissions():
        issues_fixed += 1
    else:
        issues_found += 1
    
    # Fix database
    if fix_database():
        issues_fixed += 1
    else:
        issues_found += 1
    
    # Create admin user
    if create_admin():
        issues_fixed += 1
    else:
        issues_found += 1
    
    print("=" * 50)
    print(f"✅ Issues Fixed: {issues_fixed}")
    print(f"❌ Issues Found: {issues_found}")
    
    if issues_found == 0:
        print("🎉 All issues resolved! Backend should work now.")
        print("🚀 Run 'python main.py' to start the server")
    else:
        print("⚠️ Some issues remain. Check the logs above.")
    
    return issues_found == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
