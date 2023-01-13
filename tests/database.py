from contextlib import contextmanager
from typing import Generator

import pytest
from sqlalchemy import func, select
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app.config.settings import DefaultSettings
from app.db.postgres.models import BaseAlchemyModel

test_settings = DefaultSettings()
test_settings.postgres_db += "_test"
engine = create_engine(test_settings.db_url, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def prepare_db():
    if not database_exists(test_settings.db_url):
        create_database(test_settings.db_url)
    BaseAlchemyModel.metadata.drop_all(bind=engine)
    BaseAlchemyModel.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def session(prepare_db) -> Generator:
    with TestingSessionLocal() as s:
        yield s


@contextmanager
def created_rows_count(session, model, count):
    query = select(func.count()).select_from(model)
    initial_rows_count = session.scalar(query)
    yield initial_rows_count
    assert session.scalar(query) - initial_rows_count == count
