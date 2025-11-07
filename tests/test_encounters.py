from uuid import uuid4


def test_create_encounter_returns_201(client):
    payload = dict(
        patientId=str(uuid4()),
        providerId=str(uuid4()),
        encounterType="initial_assessment",
        encounterDate="2025-01-02T03:04:05Z",
        clinicalData={"vitals": {"hr": 72, "bp": "120/80"}},
    )

    response = client.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()


def test_create_encounter_returns_generated_id(client):
    payload = dict(
        patientId=str(uuid4()),
        providerId=str(uuid4()),
        encounterType="initial_assessment",
        encounterDate="2025-01-02T03:04:05Z",
        clinicalData={"vitals": {"hr": 72, "bp": "120/80"}},
    )

    response = client.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()
    assert "encounterId" in response.json()

def test_can_get_encounter(client, created_encounter_id):
    response = client.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()