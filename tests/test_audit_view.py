from datetime import datetime, timedelta


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
