from fastapi.testclient import TestClient
from ai_test_platform.app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Test Platform API"}

def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "test project", "description": "test description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test project"
    assert data["id"] == "p_1"

def test_list_projects():
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1

def test_create_environment():
    response = client.post(
        "/projects/p_1/environments",
        json={
            "name": "test env",
            "baseUrl": "http://localhost:8000",
            "auth": {"authType": "bearer", "tokenVar": "token"},
            "variables": {"key": "value"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test env"
    assert data["projectId"] == "p_1"

def test_create_interface():
    response = client.post(
        "/interfaces/",
        json={
            "title": "test api",
            "method": "POST",
            "path": "/api/test",
            "projectId": "p_1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test api"

def test_ai_generation_flow():
    # 1. Start generation
    response = client.post(
        "/ai/generations",
        json={
            "projectId": "p_1",
            "interfaceId": "api_1",
            "envId": "env_1",
            "types": ["positive"],
            "maxCases": 1
        }
    )
    assert response.status_code == 200
    job_id = response.json()["jobId"]
    assert job_id == "job_gen_001"

    # 2. Check job status
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["status"] == "running"

    # 3. Check logs
    response = client.get(f"/jobs/{job_id}/logs")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

    # 4. Check results
    response = client.get(f"/jobs/{job_id}/results")
    assert response.status_code == 200
    data = response.json()
    assert "generatedTestcases" in data
