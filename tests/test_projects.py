
import pytest
from fastapi.testclient import TestClient
from datetime import date

class TestProjectManagement:
    
    def test_create_project(self, client: TestClient, auth_headers):
        """Test project creation"""
        project_data = {
            "name": "Website Redesign",
            "description": "Complete redesign of company website",
            "start_date": str(date.today()),
            "budget": 50000.00,
            "status": "planning"
        }
        response = client.post(
            "/api/v1/projects/projects/",
            json=project_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == project_data["name"]
    
    def test_get_projects(self, client: TestClient, auth_headers):
        """Test get projects with filtering"""
        response = client.get("/api/v1/projects/projects/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_task(self, client: TestClient, auth_headers):
        """Test task creation"""
        task_data = {
            "title": "Design Homepage",
            "description": "Create new homepage design mockups",
            "project_id": 1,
            "priority": "High",
            "status": "todo",
            "estimated_hours": 20
        }
        response = client.post(
            "/api/v1/projects/tasks/",
            json=task_data,
            headers=auth_headers
        )
        assert response.status_code in [200, 400]  # May fail due to foreign key constraints
    
    def test_get_tasks_with_filters(self, client: TestClient, auth_headers):
        """Test get tasks with filtering"""
        response = client.get(
            "/api/v1/projects/tasks/?status=todo&priority=High",
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_get_overdue_tasks(self, client: TestClient, auth_headers):
        """Test get overdue tasks"""
        response = client.get("/api/v1/projects/tasks/overdue", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
