import pytest
from starlette.testclient import TestClient

from encounter_api.fastapi_app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)
