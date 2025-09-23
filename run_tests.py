
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
    
    # Check if test dependencies are already available
    try:
        import pytest
        import httpx
        print("✅ Test dependencies already available!")
    except ImportError:
        print("❌ Test dependencies not found. Please install them manually:")
        print("   Add these packages to requirements.txt:")
        print("   - pytest>=8.0.0")
        print("   - pytest-cov>=4.0.0") 
        print("   - pytest-html>=4.0.0")
        print("   - httpx>=0.24.0")
        print("   Then restart your Repl to auto-install them.")
        return False
    
    # Run tests with coverage
    test_commands = [
        # Unit tests
        [
            "python", "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--maxfail=10"
        ]
    ]
    
    # Try to run with coverage if available
    try:
        import pytest_cov
        test_commands[0].extend([
            "--cov=app",
            "--cov-report=term-missing"
        ])
        print("✅ Running tests with coverage reporting")
    except ImportError:
        print("⚠️ Running tests without coverage (pytest-cov not available)")
    
    # Try to generate HTML report if available
    try:
        import pytest_html
        test_commands[0].extend([
            "--html=test_report.html",
            "--self-contained-html"
        ])
        print("✅ Will generate HTML test report")
    except ImportError:
        print("⚠️ HTML test report not available (pytest-html not installed)")
    
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
        except FileNotFoundError:
            print("❌ pytest not found. Please ensure pytest is installed.")
            return False
    
    print("\n✅ All tests completed successfully!")
    print("\n📊 Test Reports:")
    if os.path.exists("test_report.html"):
        print("- Test Report: test_report.html")
    if os.path.exists("htmlcov/index.html"):
        print("- Coverage Report: htmlcov/index.html")
    
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
