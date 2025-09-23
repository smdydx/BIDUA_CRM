#!/bin/bash

echo "🔨 Building React frontend for production..."
cd frontend
npm ci
npm run build
cd ..

echo "🚀 Starting production server..."
uvicorn main:app --host 0.0.0.0 --port 5000