def test_create_encounter_returns_201(client):
    payload = dict(
        patient_id="pat_123",
        provider_id="prov_456",
        encounter_datetime="2025-01-02T03:04:05Z",
        clinical_data={"vitals": {"hr": 72, "bp": "120/80"}},
    )

    response = client.post("/encounters", json=payload)
    assert response.status_code == 201
