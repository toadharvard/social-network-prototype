import pytest
from tests.database import *
from fastapi.testclient import TestClient

from app.dto.user import CreateUserSchema
from tests.overrides import app
from tests.utils import factory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_user(client: TestClient):
    user_data = factory(CreateUserSchema).build().dict()
    client.post(
        "api/auth/register",
        json=user_data,
    ).json()
    return user_data


@pytest.fixture
def auth_headers(test_user, client: TestClient):
    res = client.post(
        "api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert res.status_code == 200
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
