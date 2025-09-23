# CRM + HRMS System

## Overview
This is a comprehensive Customer Relationship Management and Human Resource Management System built with FastAPI. The application provides a complete backend API for managing customers, employees, sales pipelines, HR processes, and more.

## Current State
- **Status**: Fully functional and running in Replit environment
- **Frontend**: React development server on port 5000 with Replit proxy configuration
- **Backend**: FastAPI application on port 8000 (development) / port 5000 (production)
- **Database**: PostgreSQL with all tables created and working
- **API Documentation**: Available at `/docs` endpoint

## Recent Changes (September 23, 2025)
- **COMPLETED**: Successfully imported and configured GitHub project for Replit environment (Fresh Clone Setup)
- **INSTALLED**: Python 3.11, Node.js 20, and all required dependencies via package manager
- **CONFIGURED**: PostgreSQL database integration with automatic table creation
- **CONFIGURED**: React frontend with proper Replit proxy settings (HOST=0.0.0.0, DANGEROUSLY_DISABLE_HOST_CHECK=true)
- **CONFIGURED**: FastAPI backend with development/production mode detection
- **VERIFIED**: `start_dev.sh` script properly starts both frontend and backend
- **CONFIGURED**: Single workflow "Frontend Server" running React dev server on port 5000
- **TESTED**: Complete end-to-end functionality - both frontend and backend working perfectly
- **VERIFIED**: API endpoints tested and working (auth /api/v1/auth/login, analytics /api/v1/analytics/dashboard, health /health)
- **CONFIGURED**: Production deployment configuration (autoscale, builds React app, serves from FastAPI on port 5000)
- **VERIFIED**: Demo authentication working (admin@company.com / admin123, hr@company.com / hr123, employee@company.com / emp123)
- **FIXED**: Type annotation issues in JWT token handling for proper TypeScript compatibility
- Application is now fully functional with proper development and production configurations

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