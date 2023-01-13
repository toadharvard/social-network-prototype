from app.__main__ import get_app
from app.db.postgres.connection import get_session
from tests.database import TestingSessionLocal


def override_get_session():
    with TestingSessionLocal() as session:
        yield session


app = get_app()
app.dependency_overrides[get_session] = override_get_session
