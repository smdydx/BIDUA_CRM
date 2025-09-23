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
- Installed Python 3.11 and all required dependencies
- Migrated database configuration from SQLite to PostgreSQL
- Resolved SQLAlchemy model relationship conflicts during startup
- Configured FastAPI server workflow on port 5000 with Redis fallback
- Set up autoscale deployment configuration for production
- Verified all main endpoints are working correctly (/, /health, /docs)
- Application is fully functional and ready for use

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
- **Command**: `uvicorn main:app --host 0.0.0.0 --port 5000`
- **Port**: 5000 (configured for Replit environment)

## Technical Notes
- Uses SQLAlchemy 2.0 with proper `text()` functions for raw SQL
- FastAPI with automatic API documentation
- PostgreSQL database with comprehensive schema
- CORS enabled for all origins
- Proper validation and constraints on all models
- Extensive enum types for data integrity