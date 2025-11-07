from uuid import uuid4

from tests.builders import build_encounter_payload


def test_logging_obfuscates_clinical_data(client_1, caplog):
    payload = build_encounter_payload(clinicalData="our_secret")
    with caplog.at_level("INFO"):
        client_1.post("/encounters", json=payload)
        assert "create_encounter" in caplog.text
        assert "our_secret" not in caplog.text


def test_logging_obfuscates_patient_id(client_1, caplog):
    patient_id = uuid4()
    payload = build_encounter_payload(patient_id=patient_id)
    with caplog.at_level("INFO"):
        client_1.post("/encounters", json=payload)
        assert "create_encounter" in caplog.text
        assert str(patient_id) not in caplog.text
