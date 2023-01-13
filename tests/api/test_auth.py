import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status
from app.db.postgres import models
from app.dto.user import *
from tests.database import created_rows_count
from tests.utils import factory


class TestAuthRouter:
    @property
    def default_api_url(self):
        return "api/auth"

    @pytest.mark.parametrize("payload", factory(CreateUserSchema).batch(3))
    def test_register_new_user(
        self,
        payload: CreateUserSchema,
        client: TestClient,
        session: Session,
    ):
        with created_rows_count(session, models.User, 1):
            resp = client.post(self.default_api_url + "/register", json=payload.dict())
        assert resp.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("payload", factory(CreateUserSchema).batch(3))
    def test_register_already_exist(
        self,
        payload: CreateUserSchema,
        client: TestClient,
        session: Session,
    ):
        resp = client.post(self.default_api_url + "/register", json=payload.dict())
        assert resp.status_code == status.HTTP_200_OK
        with created_rows_count(session, models.User, 0):
            resp = client.post(self.default_api_url + "/register", json=payload.dict())
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("_", range(3))
    def test_delete_user(
        self,
        client: TestClient,
        session: Session,
        auth_headers,
        _,
    ):
        with created_rows_count(session, models.User, -1):
            resp = client.delete(
                self.default_api_url + "/takeout", headers=auth_headers
            )
        assert resp.status_code == status.HTTP_200_OK

    def test_login_existing_user(self, test_user: dict, client: TestClient):
        resp = client.post(
            self.default_api_url + "/login",
            data={
                "username": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert resp.status_code == status.HTTP_200_OK

    def test_login_not_existing_user(self, client: TestClient):
        resp = client.post(
            self.default_api_url + "/login",
            data={
                "username": "NotExistingRandomUsername@mail.com",
                "password": "fakepassword",
            },
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
