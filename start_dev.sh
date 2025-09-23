#!/bin/bash

echo "🚀 Starting CRM + HRMS Pro Development Environment..."

# Create database tables
echo "🗄️ Setting up database..."
python create_tables.py

# Start backend server in background
echo "🔧 Starting FastAPI backend server..."
python main.py &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Check if backend started successfully
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend server is running on localhost:8000"
else
    echo "❌ Backend server failed to start"
    exit 1
fi

echo "🎨 Starting React frontend..."
echo ""
echo "🌐 Application will be available at:"
echo "   https://$REPLIT_DEV_DOMAIN (Replit URL)"
echo "   http://localhost:5000 (if accessing directly)"
echo ""
echo "📋 Demo Login Credentials:"
echo "   📧 Email: admin@company.com"
echo "   🔑 Password: admin123"
echo ""

# Start React development server (main process)
cd frontend
exec npm start