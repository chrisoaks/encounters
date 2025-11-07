import pytest


@pytest.mark.parametrize(
    "api_key, expected_status_code", [
        ("secret123", 200),
        ("invalid", 403),
    ]
)
def test_api_key_matters(unauthenticated_client, api_key, expected_status_code):
    unauthenticated_client.headers["X-API-Key"] = api_key
    response = unauthenticated_client.get("/audit/encounters")
    assert response.status_code == expected_status_code, response.json()
