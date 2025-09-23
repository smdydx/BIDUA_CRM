
import pytest
from fastapi.testclient import TestClient

class TestDataValidation:
    
    def test_user_email_validation(self, client: TestClient, auth_headers):
        """Test email validation for user creation"""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user.domain",
            ""
        ]
        
        for invalid_email in invalid_emails:
            user_data = {
                "username": "testuser",
                "email": invalid_email,
                "first_name": "Test",
                "last_name": "User",
                "password": "password123"
            }
            response = client.post("/api/v1/users/", json=user_data, headers=auth_headers)
            assert response.status_code == 422  # Validation error
    
    def test_employee_id_format_validation(self, client: TestClient, auth_headers):
        """Test employee ID format validation"""
        invalid_employee_ids = [
            "123",  # No EMP prefix
            "EMP",  # No numbers
            "EMP12",  # Too short
            "EMPLOYEE001",  # Wrong prefix
        ]
        
        for invalid_id in invalid_employee_ids:
            employee_data = {
                "employee_id": invalid_id,
                "user_id": 1,
                "hire_date": "2024-01-01",
                "salary": 50000.00
            }
            response = client.post("/api/v1/hr/employees/", json=employee_data, headers=auth_headers)
            assert response.status_code == 422  # Validation error
    
    def test_deal_value_validation(self, client: TestClient, auth_headers):
        """Test deal value validation"""
        invalid_values = [-1000, 0, 100000001]  # Negative, zero, too large
        
        for invalid_value in invalid_values:
            deal_data = {
                "title": "Test Deal",
                "company_id": 1,
                "stage": "prospecting",
                "value": invalid_value,
                "probability": 50
            }
            response = client.post("/api/v1/crm/deals/", json=deal_data, headers=auth_headers)
            assert response.status_code == 422  # Validation error
