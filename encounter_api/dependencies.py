from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request


def get_encounter_repository(request: Request):
    return request.app.state.encounter_repository


USERS = {
    "secret123": "user_1",
    "secret456": "user_2",
}

api_key_header = APIKeyHeader(name="X-API-Key")


def get_current_user(api_key: str = Security(api_key_header)):
    if api_key not in USERS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return USERS[api_key]
