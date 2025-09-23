
#!/bin/bash

echo "🚀 Starting CRM + HRMS Pro Application..."

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Create database tables
echo "🗄️ Setting up database..."
python create_tables.py

# Create admin user
echo "👤 Creating admin user..."
python create_admin_user.py

# Start backend server in background
echo "🔧 Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
cd frontend && BROWSER=none npm start &
FRONTEND_PID=$!

echo "✅ Application started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "📋 Demo Login Credentials:"
echo "📧 Email: admin@company.com"
echo "🔑 Password: admin123"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
