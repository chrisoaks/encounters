from tests.builders import build_encounter_payload


def test_create_encounter_returns_201(client_1):
    payload = build_encounter_payload()

    response = client_1.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()


def test_create_encounter_returns_generated_id(client_1):
    payload = build_encounter_payload()

    response = client_1.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()
    assert "encounterId" in response.json()


def test_create_encounter_clinical_data_can_be_number(client_1):
    payload = build_encounter_payload(clinicalData=5)

    response = client_1.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()
    assert "encounterId" in response.json()


def test_can_get_encounter(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()


def test_a_user_must_be_authenticated_to_get_encounter(unauthenticated_client, created_encounter_id):
    response = unauthenticated_client.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 403, response.json()

def test_an_authenticated_user_can_get_encounter(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()
