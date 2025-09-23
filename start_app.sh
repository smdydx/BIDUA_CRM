#!/bin/bash

# Start the FastAPI backend on port 8000
echo "🚀 Starting FastAPI backend on port 8000..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start the React frontend on port 5000
echo "🚀 Starting React frontend on port 5000..."
cd frontend
npm start

# If the frontend stops, kill the backend too
kill $BACKEND_PID 2>/dev/null