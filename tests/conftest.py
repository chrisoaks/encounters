import pytest
from starlette.testclient import TestClient

from encounter_api.fastapi_app import create_app
from tests.builders import build_encounter_payload


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client_1(app):
    return TestClient(
        app,
        headers={"X-API-Key": "secret123"},
    )


@pytest.fixture
def client_2(app):
    return TestClient(
        app,
        headers={"X-API-Key": "secret456"},
    )


@pytest.fixture
def unauthenticated_client(app):
    return TestClient(
        app,
    )


@pytest.fixture
def created_encounter_id(client_1):
    payload = build_encounter_payload()
    response = client_1.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()
    return response.json()["encounterId"]
