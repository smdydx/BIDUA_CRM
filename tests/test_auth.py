
import pytest
from fastapi.testclient import TestClient

class TestAuthentication:
    
    def test_login_endpoint(self, client: TestClient):
        """Test user login endpoint"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "password"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_get_current_user(self, client: TestClient, auth_headers):
        """Test get current user endpoint"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
    
    def test_refresh_token(self, client: TestClient, auth_headers):
        """Test token refresh endpoint"""
        response = client.post("/api/v1/auth/refresh", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_unauthorized_access(self, client: TestClient):
        """Test unauthorized access"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
