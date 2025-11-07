from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from encounter_api.enums import EncounterType
from encounter_api.types import SecretJson, SecretUUID


@dataclass(kw_only=True)
class EncounterMetadata:
    createdAt: datetime = field(default_factory=datetime.utcnow)
    updatedAt: datetime = field(default_factory=datetime.utcnow)
    createdBy: str


@dataclass(kw_only=True)
class AccessEvent:
    accessedOn: datetime = field(default_factory=datetime.utcnow)
    accessedBy: str


@dataclass(kw_only=True)
class EncounterState:
    encounter_id: UUID = field(default_factory=uuid4)
    patient_id: SecretUUID
    provider_id: UUID
    encounter_datetime: datetime
    encounter_type: EncounterType
    clinical_data: SecretJson
    metadata: EncounterMetadata
    accesses: list[AccessEvent] = field(default_factory=list)


class EncounterException(Exception):
    pass


class EncounterRepository:
    def __init__(self) -> None:
        self.encounters: dict[UUID, EncounterState] = defaultdict()

    def add_encounter(
        self,
        patient_id: SecretUUID,
        provider_id: UUID,
        encounter_datetime: datetime,
        encounter_type: EncounterType,
        clinical_data: SecretJson,
        created_by: str,
    ) -> EncounterState:
        encounter = EncounterState(
            patient_id=patient_id,
            provider_id=provider_id,
            encounter_datetime=encounter_datetime,
            encounter_type=encounter_type,
            clinical_data=clinical_data,
            metadata=EncounterMetadata(createdBy=created_by),
        )
        self.encounters[encounter.encounter_id] = encounter
        return encounter

    def get_encounter(self, encounter_id: UUID, user_id: str) -> EncounterState:
        try:
            encounter = self.encounters[encounter_id]
        except KeyError:
            raise EncounterException(f"Encounter {encounter_id} not found")
        encounter.accesses.append(AccessEvent(accessedBy=user_id))
        return encounter

    def list_encounters(self) -> list[EncounterState]:
        return list(self.encounters.values())

def get_encounter_repository(request: Request):
    return request.app.state.encounter_repository


USERS = {
    "secret123": "user_1",
    "secret456": "user_2",
}

api_key_header = APIKeyHeader(name="X-API-Key")


def get_current_user(api_key: str = Security(api_key_header)):
    if api_key not in USERS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return USERS[api_key]
