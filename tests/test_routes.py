import json

# health check test
def test_health(client) -> None:
    response = client.get("/health")
    assert response.json == {"status": "healthy"}
    assert response.status_code == 200

# get all users
def test_get_users(client) -> None:
    response = client.get("/user")
    assert response.json == [{"id": 1, "name": "adam", "email": "januszek@domain.com"}, {"id": 2, "name": "ala", "email": "ala@domain.com"}]
    assert response.status_code == 200

# get user by id
def test_get_user_by_id(client) -> None:
    response = client.get("/user/1")
    assert response.json == {"id": 1, "name": "adam", "email": "januszek@domain.com"}
    assert response.status_code == 200

# create user
def test_create_user(client) -> None:
    # happy path
    response = client.post("/user", data=json.dumps({"name": "John", "email": "john@msn.com"}), headers={'Content-Type': 'application/json'})
    assert response.json == {'message': 'user created successfully'}
    assert response.status_code == 201

    # error handling
    response = client.post("/user", data=json.dumps({"name": "John"}), headers={'Content-Type': 'application/json'})
    assert response.json == {'error': 'missing data.'}
    assert response.status_code == 404

    response = client.post("/user", data=json.dumps({"name": "adam", "email": "januszek@domain.com"}), headers={'Content-Type': 'application/json'})
    assert response.json == {'error': 'user creation failed.'}
    assert response.status_code == 409

def test_delete_user(client) -> None:
    # happy path
    response = client.delete("/user/1")
    assert response.json == {'message': 'user deleted successfully'}
    assert response.status_code == 200
 
    # error handling
    response = client.delete("/user/100")
    assert response.json == {'error': 'user not found.'}
    assert response.status_code == 419
    