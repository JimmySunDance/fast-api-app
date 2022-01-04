from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to my API"
    assert res.status_code == 200


def test_crete_user(client):
    res = client.post(
        "/users/", json={"email": "testemail@test.com", "password": "password123"}
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "testemail@test.com"
    assert res.status_code == 201


def test_login_user(client):
    res = client.post(
        "/login/", data={"username": "testemail@test.com", "password": "password123"}
    )
    print(res.json)
    assert res.status_code == 200