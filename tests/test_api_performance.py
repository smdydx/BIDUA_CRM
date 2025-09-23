
import pytest
import time
from fastapi.testclient import TestClient

class TestAPIPerformance:
    
    def test_api_response_time(self, client: TestClient):
        """Test API response times are under acceptable limits"""
        endpoints = [
            "/",
            "/health",
            "/openapi.json"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response.status_code == 200
            assert response_time < 1.0  # Should respond within 1 second
    
    def test_authenticated_endpoints_performance(self, client: TestClient, auth_headers):
        """Test authenticated endpoints performance"""
        endpoints = [
            "/api/v1/auth/me",
            "/api/v1/users/",
            "/api/v1/crm/companies/",
            "/api/v1/hr/departments/",
            "/api/v1/projects/projects/",
            "/api/v1/analytics/dashboard"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint, headers=auth_headers)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response.status_code == 200
            assert response_time < 2.0  # Should respond within 2 seconds
    
    def test_pagination_performance(self, client: TestClient, auth_headers):
        """Test pagination performance with different page sizes"""
        page_sizes = [10, 20, 50, 100]
        
        for size in page_sizes:
            start_time = time.time()
            response = client.get(f"/api/v1/users/?page=1&size={size}", headers=auth_headers)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response.status_code == 200
            assert response_time < 3.0  # Larger page sizes should still be fast
