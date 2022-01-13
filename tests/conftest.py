import pytest
from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app.config import settings
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user_1(client):
    user_data = {"email": "testemail_1@test.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_2(client):
    user_data = {"email": "testemail_2@test.com", "password": "password321"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user_1):
    return create_access_token({"user_id": test_user_1["id"]})


@pytest.fixture
def authorised_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user_1, test_user_2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user_1["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user_1["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user_1["id"],
        },
        {
            "title": "COPY third title",
            "content": "COPY third content",
            "owner_id": test_user_2["id"],
        },
    ]

    post_map = map(lambda x: models.Post(**x), posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    
    return session.query(models.Post).all()
