from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test API Task",
            "description": "This is a test task created via API",
            "status": "pending",
            "priority": "medium",
            "category": "API Test",
            "due_date": "2023-12-31T23:59:59"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test API Task"
    assert "id" in data


def test_read_tasks():
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_task():
    # First, create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task to Read"}
    )
    create_data = create_response.json()
    task_id = create_data["id"]

    # Then, read the task
    read_response = client.get(f"/api/v1/tasks/{task_id}")
    assert read_response.status_code == 200
    read_data = read_response.json()
    assert read_data["id"] == task_id
    assert read_data["title"] == "Task to Read"


def test_update_task():
    # First, create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task to Update"}
    )
    create_data = create_response.json()
    task_id = create_data["id"]

    # Then, update the task
    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "status": "completed"
        }
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["id"] == task_id
    assert update_data["title"] == "Updated Task"
    assert update_data["status"] == "completed"


def test_delete_task():
    # First, create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task to Delete"}
    )
    create_data = create_response.json()
    task_id = create_data["id"]

    # Then, delete the task
    delete_response = client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_response.status_code == 200

    # Verify that the task is deleted
    read_response = client.get(f"/api/v1/tasks/{task_id}")
    assert read_response.status_code == 404
