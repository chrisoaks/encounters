from datetime import datetime, timedelta
from uuid import uuid4

from tests.builders import build_encounter_payload


def test_create_encounter_returns_201(client_1):
    payload = build_encounter_payload()

    response = client_1.post("/encounters", json=payload)
    assert response.status_code == 201, response.json()


def test_logging_obfuscates_clinical_data(client_1, caplog):
    payload = build_encounter_payload(clinicalData="our_secret")
    with caplog.at_level("INFO"):
        client_1.post("/encounters", json=payload)
        assert "our_secret" not in caplog.text


def test_logging_obfuscates_patient_id(client_1, caplog):
    patient_id = uuid4()
    payload = build_encounter_payload(patient_id=patient_id)
    with caplog.at_level("INFO"):
        client_1.post("/encounters", json=payload)
        assert str(patient_id) not in caplog.text


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


def test_can_get_encounter_can_404(client_1):
    response = client_1.get(f"/encounters/{str(uuid4())}")
    assert response.status_code == 404, response.json()


def test_can_get_encounter(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()


def test_a_user_must_be_authenticated_to_get_encounter(
    unauthenticated_client, created_encounter_id
):
    response = unauthenticated_client.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 403, response.json()


def test_an_authenticated_user_can_get_encounter(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()


def test_list_audit_events_requires_auth(unauthenticated_client):
    response = unauthenticated_client.get("/audit/encounters")
    assert response.status_code == 403, response.json()


def test_list_audit_events_initially_empty(client_1):
    response = client_1.get("/audit/encounters")
    assert response.status_code == 200, response.json()
    assert response.json() == []


def test_a_created_encounter_is_audited(client_1, created_encounter_id):
    response = client_1.get("/audit/encounters")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1
    assert response.json()[0]["encounterId"] == created_encounter_id
    assert response.json()[0]["accessType"] == "write"


def test_a_viewed_encounter_is_audited(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()
    response = client_1.get("/audit/encounters")
    assert len(response.json()) == 2

    assert response.json()[1]["encounterId"] == created_encounter_id
    assert response.json()[1]["accessType"] == "read"


def test_audit_events_can_be_filtered_by_start_date(client_1, created_encounter_id):
    # Get the audit event first to get its timestamp
    response = client_1.get("/audit/encounters")
    audit_timestamp = datetime.fromisoformat(
        response.json()[0]["accessedOn"].replace("Z", "+00:00")
    )

    # Filter with start date after the event - should return empty
    future_date = (audit_timestamp + timedelta(days=1)).isoformat()
    response = client_1.get(f"/audit/encounters?startDateTime={future_date}")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 0

    # Filter with start date before the event - should return the event
    past_date = (audit_timestamp - timedelta(days=1)).isoformat()
    response = client_1.get(f"/audit/encounters?startDateTime={past_date}")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1


def test_audit_events_can_be_filtered_by_end_date(client_1, created_encounter_id):
    # Get the audit event first to get its timestamp
    response = client_1.get("/audit/encounters")
    audit_timestamp = datetime.fromisoformat(
        response.json()[0]["accessedOn"].replace("Z", "+00:00")
    )

    # Filter with end date before the event - should return empty
    past_date = (audit_timestamp - timedelta(days=1)).isoformat()
    response = client_1.get(f"/audit/encounters?endDateTime={past_date}")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 0

    # Filter with end date after the event - should return the event
    future_date = (audit_timestamp + timedelta(days=1)).isoformat()
    response = client_1.get(f"/audit/encounters?endDateTime={future_date}")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1
