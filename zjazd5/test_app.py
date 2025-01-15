import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# GET /users
def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# GET /users/{id}
def test_get_user_existing(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Jan Kowalski"

def test_get_user_nonexistent(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

# POST /users
def test_create_user_success(client):
    new_user = {"name": "Adam Mickiewicz", "email": "adam@mickiewicz.pl"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]

def test_create_user_invalid(client):
    response = client.post("/users", json={"name": "No Email"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid input"

# PUT /users/{id}
def test_update_user_success(client):
    updated_data = {"name": "Jan Kowalski Updated", "email": "jan.updated@kowalski.pl"}
    response = client.put("/users/1", json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]

def test_update_user_nonexistent(client):
    response = client.put("/users/999", json={"name": "Fake User", "email": "fake@user.pl"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

def test_update_user_invalid(client):
    response = client.put("/users/1", json={"name": "Incomplete"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid input"

# DELETE /users/{id}
def test_delete_user_success(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted"

def test_delete_user_nonexistent(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"
