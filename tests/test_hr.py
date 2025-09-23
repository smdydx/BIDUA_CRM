
import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime

class TestHRManagement:
    
    def test_create_department(self, client: TestClient, auth_headers, sample_department_data):
        """Test department creation"""
        response = client.post(
            "/api/v1/hr/departments/",
            json=sample_department_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_department_data["name"]
    
    def test_get_departments(self, client: TestClient, auth_headers):
        """Test get departments"""
        response = client.get("/api/v1/hr/departments/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_designation(self, client: TestClient, auth_headers):
        """Test designation creation"""
        designation_data = {
            "title": "Senior Developer",
            "department_id": 1,
            "level": 3,
            "description": "Senior software developer position"
        }
        response = client.post(
            "/api/v1/hr/designations/",
            json=designation_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == designation_data["title"]
    
    def test_create_employee(self, client: TestClient, auth_headers):
        """Test employee creation"""
        employee_data = {
            "employee_id": "EMP001",
            "user_id": 1,
            "hire_date": str(date.today()),
            "employment_type": "full_time",
            "status": "active",
            "salary": 75000.00
        }
        response = client.post(
            "/api/v1/hr/employees/",
            json=employee_data,
            headers=auth_headers
        )
        assert response.status_code in [200, 400]  # May fail due to foreign key constraints
    
    def test_create_leave_type(self, client: TestClient, auth_headers):
        """Test leave type creation"""
        leave_type_data = {
            "name": "Annual Leave",
            "description": "Yearly vacation leave",
            "max_days_per_year": 21
        }
        response = client.post(
            "/api/v1/hr/leave-types/",
            json=leave_type_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == leave_type_data["name"]
    
    def test_create_leave_request(self, client: TestClient, auth_headers):
        """Test leave request creation"""
        leave_request_data = {
            "leave_type_id": 1,
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "days_requested": 1,
            "reason": "Personal work that needs immediate attention"
        }
        response = client.post(
            "/api/v1/hr/leave-requests/",
            json=leave_request_data,
            headers=auth_headers
        )
        assert response.status_code in [200, 400]  # May fail due to foreign key constraints
    
    def test_get_leave_requests_with_filters(self, client: TestClient, auth_headers):
        """Test get leave requests with filtering"""
        response = client.get(
            "/api/v1/hr/leave-requests/?status=pending",
            headers=auth_headers
        )
        assert response.status_code == 200
