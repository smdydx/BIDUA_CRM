
import pytest
from fastapi.testclient import TestClient

class TestCRMManagement:
    
    def test_create_company(self, client: TestClient, auth_headers, sample_company_data):
        """Test company creation"""
        response = client.post(
            "/api/v1/crm/companies/",
            json=sample_company_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_company_data["name"]
        assert data["industry"] == sample_company_data["industry"]
    
    def test_get_companies(self, client: TestClient, auth_headers):
        """Test get companies with search"""
        response = client.get("/api/v1/crm/companies/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_companies(self, client: TestClient, auth_headers):
        """Test company search functionality"""
        response = client.get(
            "/api/v1/crm/companies/?search=technology&industry=Technology",
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_contact(self, client: TestClient, auth_headers):
        """Test contact creation"""
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "job_title": "Manager",
            "company_id": 1,
            "is_primary": True
        }
        response = client.post(
            "/api/v1/crm/contacts/",
            json=contact_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
    
    def test_create_lead(self, client: TestClient, auth_headers):
        """Test lead creation"""
        lead_data = {
            "title": "New Business Opportunity",
            "source": "Website",
            "status": "new",
            "estimated_value": 50000.00,
            "probability": 25,
            "description": "Potential client interested in our services"
        }
        response = client.post(
            "/api/v1/crm/leads/",
            json=lead_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == lead_data["title"]
        assert data["status"] == "new"
    
    def test_create_deal(self, client: TestClient, auth_headers):
        """Test deal creation"""
        deal_data = {
            "title": "Software License Deal",
            "stage": "prospecting",
            "value": 75000.00,
            "probability": 50,
            "company_id": 1,
            "description": "Annual software license renewal"
        }
        response = client.post(
            "/api/v1/crm/deals/",
            json=deal_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == deal_data["title"]
        assert float(data["value"]) == deal_data["value"]
    
    def test_get_revenue_by_stage(self, client: TestClient, auth_headers):
        """Test revenue analytics by deal stage"""
        response = client.get("/api/v1/crm/deals/revenue/by-stage", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
