def test_health(client) -> None:
    rv = client.get("/health")
    assert rv.json == {"status": "healthy"}

def test_get_user_by_id(client) -> None:
    rv = client.get("/user/1")
    assert rv.json == {"id": 1, "name": "adam", "email": "januszek@domain.com"}