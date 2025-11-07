from uuid import uuid4


def build_encounter_payload(
    patient_id=uuid4(),
    clinicalData=None,
):
    if clinicalData is None:
        clinicalData = {"vitals": {"hr": 72, "bp": "120/80"}}
    return dict(
        patientId=str(patient_id),
        providerId=str(uuid4()),
        encounterType="initial_assessment",
        encounterDate="2025-01-02T03:04:05Z",
        clinicalData=clinicalData,
    )
