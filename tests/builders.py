from uuid import uuid4


def build_encounter_payload(
    clinicalData=None,
):
    if clinicalData is None:
        clinicalData = {"vitals": {"hr": 72, "bp": "120/80"}}
    return dict(
        patientId=str(uuid4()),
        providerId=str(uuid4()),
        encounterType="initial_assessment",
        encounterDate="2025-01-02T03:04:05Z",
        clinicalData=clinicalData,
    )
