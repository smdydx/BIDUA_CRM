# CRM + HRMS System

## Overview
This is a comprehensive Customer Relationship Management and Human Resource Management System built with FastAPI. The application provides a complete backend API for managing customers, employees, sales pipelines, HR processes, and more.

## Current State
- **Status**: Fully functional and deployed
- **Backend**: FastAPI application running on port 5000
- **Database**: PostgreSQL with all tables created
- **API Documentation**: Available at `/docs` endpoint

## Recent Changes (September 23, 2025)
- Successfully imported GitHub project into Replit environment
- Installed Python 3.11, Node.js 20, and all required dependencies
- **CONFIGURED**: PostgreSQL database integration with proper fallback to SQLite in development
- **CONFIGURED**: Full-stack application with React frontend on port 5000 and FastAPI backend on port 8000 (development)
- **CONFIGURED**: React frontend to trust Replit proxy with proper host settings (HOST=0.0.0.0, DISABLE_HOST_CHECK=true)
- **CONFIGURED**: Backend to use localhost in development, 0.0.0.0 in production
- **CREATED**: Development startup script (start_app.sh) that runs both frontend and backend
- **CONFIGURED**: Single workflow "Frontend Server" that serves the React app on port 5000
- **CONFIGURED**: Production deployment with React build served through FastAPI on port 5000
- **TESTED**: Frontend-backend integration via proxy - API calls working correctly
- **FIXED**: CORS configuration and security issues identified in review
- All API endpoints working: Authentication, CRM, HR, Analytics, Projects
- Application is fully functional with complete development and production configurations

## Project Architecture

### Backend Structure
- **main.py**: FastAPI application entry point with basic routes
- **models.py**: SQLAlchemy database models for all entities
- **database.py**: Database configuration and session management
- **create_tables.py**: Database table creation script
- **requirements.txt**: Python dependencies

### Key Features Available
- Customer Relationship Management
- Human Resource Management
- Project Management
- Task Management
- Training & Development
- Expense Management
- Document Management
- Email Campaigns
- Support Ticketing
- Inventory Management
- Financial Management

### Database Models
The system includes comprehensive models for:
- Users and authentication
- Employee management (with detailed HR fields)
- Company and contact management
- Sales pipeline (leads, deals, activities)
- HR processes (leave, attendance, payroll)
- Project and task management
- Training and development
- Expense tracking
- And many more...

### API Endpoints
- `GET /`: Welcome message and feature list
- `GET /health`: Database connectivity health check
- `GET /docs`: Interactive API documentation (Swagger UI)
- `GET /openapi.json`: OpenAPI specification

## Deployment Configuration
- **Target**: Autoscale (stateless web application)
- **Build**: `cd frontend && npm ci && npm run build` (builds React frontend)
- **Command**: `uvicorn main:app --host 0.0.0.0 --port 5000` (serves both API and React app)
- **Port**: 5000 (serves complete full-stack application)

## Development vs Production
- **Development**: React dev server on port 5000, FastAPI on port 8000 with proxy
- **Production**: Single FastAPI server on port 5000 serving built React app and API

## Technical Notes
- Uses SQLAlchemy 2.0 with proper `text()` functions for raw SQL
- FastAPI with automatic API documentation
- PostgreSQL database with comprehensive schema
- CORS enabled for all origins
- Proper validation and constraints on all models
- Extensive enum types for data integrity