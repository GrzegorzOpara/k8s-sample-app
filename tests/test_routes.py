import json
from unittest.mock import patch

from app.routes import bp
from tests.conftest import UserFactory  # Assuming UserFactory in conftest.py


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Message" in data
    assert data["Message"].startswith("app up and running successfully")


def test_get_users_empty(client, mocker):
    # Mock the User query to return an empty list
    mocker.patch.object(bp, "get_users", return_value=[])
    response = client.get("/user")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "meta" in data
    assert "users" in data
    assert data["users"] == []


def test_get_users(client, user_factory):
    # Create some users in the test database
    users = user_factory.create_batch(2)

    response = client.get("/user")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "meta" in data
    assert "users" in data
    # Assert user data is present and matches created users
    assert len(data["users"]) == len(users)
    for i, user_data in enumerate(data["users"]):
        assert user_data["id"] == users[i].id
        assert user_data["name"] == users[i].name
        assert user_data["email"] == users[i].email


def test_get_user_by_id_not_found(client):
    response = client.get("/user/1")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "meta" in data
    assert "error" in data
    assert data["error"] == "User not found"


def test_get_user_by_id(client, user_factory):
    user = user_factory.create()

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "meta" in data
    assert "user" in data
    assert data["user"]["id"] == user.id
    assert data["user"]["name"] == user.name
    assert data["user"]["email"] == user.email


def test_update_user_not_found(client):
    data = {"username": "updated_user", "email": "updated@example.com"}
    response = client.put("/user/1", json=data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "meta" in data
    assert "message" in data
    assert data["message"] == "User not found"


def test_update_user(client, user_factory):
    user = user_factory.create()
    data = {"username": "updated_user", "email": "updated@example.com"}

    response = client.put(f"/user/{user.id}", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "meta" in data
    assert "message" in data
    assert data["message"] == "User updated successfully"

    # Check if user was actually updated
    updated_user = client.get(f"/user/{user.id}").json()["user"]
    assert updated_user["username"] == data["username"]
    assert updated_user["email"] == data["email"]


@patch("app.routes.db.session.add")
@patch("app.routes.db.session.commit")
def test_create_user_success(mock_commit, mock_add, client):
    data = {"name": "John Doe", "email": "john.doe@example.com"}
    response = client.post("/user", json=data)
    assert response.status_code == 201
    data = json.loads(response.data)