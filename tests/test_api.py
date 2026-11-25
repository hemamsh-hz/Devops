"""Small regression suite used by Jenkins and GitHub Actions."""
import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture(autouse=True)
def reset_in_memory_store():
    main._tasks.clear()
    main._next_id = 1
    yield
    main._tasks.clear()
    main._next_id = 1


@pytest.fixture
def client():
    return TestClient(main.app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_then_list_task(client):
    created = client.post("/todos", json={"title": "Write report"})
    assert created.status_code == 201
    assert created.json() == {"id": 1, "title": "Write report", "completed": False}
    listed = client.get("/todos")
    assert listed.status_code == 200
    assert listed.json()[0]["title"] == "Write report"


def test_unknown_task_returns_404(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_task_title_must_not_be_blank(client):
    response = client.post("/todos", json={"title": "   "})
    assert response.status_code == 422


def test_root_returns_service_information(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "service": "task-api",
        "message": "Task Management API is running",
        "docs": "/docs",
    }
