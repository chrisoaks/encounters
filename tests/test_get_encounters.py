from uuid import uuid4


def test_can_get_encounter_can_404(client_1):
    response = client_1.get(f"/encounters/{str(uuid4())}")
    assert response.status_code == 404, response.json()


def test_can_get_encounter(client_1, created_encounter_id):
    response = client_1.get(f"/encounters/{created_encounter_id}")
    assert response.status_code == 200, response.json()