
#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import threading

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI Backend Server...")
    try:
        subprocess.run([sys.executable, "main.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n❌ Backend server stopped")

def start_frontend():
    """Start the React frontend server"""
    print("🚀 Starting React Frontend Server...")
    time.sleep(3)  # Wait for backend to start
    try:
        os.chdir("frontend")
        # Install dependencies if needed
        if not os.path.exists("node_modules"):
            print("📦 Installing React dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start React dev server
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n❌ Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🌟 Starting CRM + HRMS Full Stack Application")
    print("=" * 50)
    print("Backend will run on: http://localhost:5000")
    print("Frontend will run on: http://localhost:3000")
    print("API Documentation: http://localhost:5000/docs")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
