
import pytest
from fastapi.testclient import TestClient

class TestAnalytics:
    
    def test_dashboard_analytics(self, client: TestClient, auth_headers):
        """Test dashboard analytics endpoint"""
        response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = [
            "total_users", "total_employees", "total_companies",
            "total_leads", "total_deals", "total_projects", 
            "total_tasks", "revenue_by_stage"
        ]
        
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], (int, dict))
        
        # Revenue by stage should be a dictionary
        assert isinstance(data["revenue_by_stage"], dict)
