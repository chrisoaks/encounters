from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from encounter_api.fastapi_app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def created_encounter_id(client):
    payload = dict(
        patientId=str(uuid4()),
        providerId=str(uuid4()),
        encounterType="initial_assessment",
        encounterDate="2025-01-02T03:04:05Z",
        clinicalData={"vitals": {"hr": 72, "bp": "120/80"}},
    )
    response = client.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()
    return response.json()["encounterId"]
