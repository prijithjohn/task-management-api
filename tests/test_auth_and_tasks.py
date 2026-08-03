from fastapi.testclient import TestClient


def test_register_and_login_and_task_flow(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["access_token"]
    assert token

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "user@example.com"

    create_task = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Write tests", "description": "Add coverage", "status": "pending", "priority": "high"},
    )
    assert create_task.status_code == 201
    task_id = create_task.json()["id"]

    list_response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["title"] == "Write tests"

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 200

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "done"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 204
