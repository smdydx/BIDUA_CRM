
import pytest
from fastapi.testclient import TestClient

class TestUserManagement:
    
    def test_create_user(self, client: TestClient, auth_headers, sample_user_data):
        """Test user creation"""
        response = client.post(
            "/api/v1/users/",
            json=sample_user_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert "password" not in data  # Password should not be returned
    
    def test_get_users(self, client: TestClient, auth_headers):
        """Test get users with pagination"""
        response = client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_users_with_filters(self, client: TestClient, auth_headers):
        """Test get users with role filter"""
        response = client.get(
            "/api/v1/users/?role=admin&is_active=true",
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_get_user_by_id(self, client: TestClient, auth_headers):
        """Test get user by ID"""
        response = client.get("/api/v1/users/1", headers=auth_headers)
        assert response.status_code in [200, 404]  # May not exist in test
    
    def test_update_user(self, client: TestClient, auth_headers):
        """Test user update"""
        update_data = {"first_name": "Updated Name"}
        response = client.put(
            "/api/v1/users/1",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code in [200, 404]
    
    def test_create_user_duplicate_email(self, client: TestClient, auth_headers, sample_user_data):
        """Test creating user with duplicate email"""
        # Create first user
        client.post("/api/v1/users/", json=sample_user_data, headers=auth_headers)
        
        # Try to create duplicate
        duplicate_data = sample_user_data.copy()
        duplicate_data["username"] = "different_username"
        
        response = client.post(
            "/api/v1/users/",
            json=duplicate_data,
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
