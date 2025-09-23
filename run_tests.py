
#!/usr/bin/env python3
"""
Test Runner Script for CRM + HRMS System
Run all tests with coverage reporting
"""

import os
import sys
import subprocess

def run_tests():
    """Run all tests with coverage"""
    
    print("🚀 Starting CRM + HRMS System Test Suite...")
    print("=" * 60)
    
    # Install test dependencies
    test_packages = [
        "pytest",
        "pytest-cov", 
        "pytest-html",
        "httpx"  # For TestClient
    ]
    
    print("📦 Installing test dependencies...")
    for package in test_packages:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    
    # Run tests with coverage
    test_commands = [
        # Unit tests
        [
            "python", "-m", "pytest", 
            "tests/", 
            "-v", 
            "--cov=app",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--html=test_report.html",
            "--self-contained-html"
        ]
    ]
    
    for cmd in test_commands:
        print(f"\n🧪 Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"❌ Test failed with exit code {e.returncode}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return False
    
    print("\n✅ All tests completed successfully!")
    print("\n📊 Test Reports:")
    print("- HTML Coverage Report: htmlcov/index.html")
    print("- Test Report: test_report.html")
    
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
