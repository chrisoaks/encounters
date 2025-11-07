import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel, Field

from encounter_api.dependencies import (
    get_encounter_repository,
    EncounterRepository,
    EncounterState,
    get_current_user,
)
from encounter_api.enums import EncounterType
from encounter_api.types import SecretJson, SecretUUID

logger = logging.getLogger(__name__)

class AuthenticatedRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependencies.append(Depends(get_current_user))

router = AuthenticatedRouter()


class CreateEncounterRequest(BaseModel):
    patient_id: SecretUUID = Field(alias="patientId")
    provider_id: UUID = Field(alias="providerId")
    encounter_date: datetime = Field(alias="encounterDate")
    encounter_type: EncounterType = Field(alias="encounterType")
    clinical_data: SecretJson = Field(alias="clinicalData")

    class Config:
        populate_by_name = True
        alias_generator = None


class EncounterMetadata(BaseModel):
    createdAt: datetime
    updatedAt: datetime
    createdBy: str


class GetEncounterResponse(BaseModel):
    encounterId: UUID
    patientId: SecretUUID
    providerId: UUID
    encounterDate: datetime
    encounterType: EncounterType
    clinicalData: SecretJson
    metadata: EncounterMetadata

    @classmethod
    def from_encounter(cls, encounter: EncounterState):
        return cls(
            encounterId=encounter.encounter_id,
            patientId=encounter.patient_id,
            providerId=encounter.provider_id,
            encounterDate=encounter.encounter_datetime,
            encounterType=encounter.encounter_type,
            clinicalData=encounter.clinical_data,
            metadata=EncounterMetadata(
                createdAt=encounter.metadata.createdAt,
                updatedAt=encounter.metadata.updatedAt,
                createdBy=encounter.metadata.createdBy,
            ),
        )


@router.post("/encounters", status_code=201)
def create_encounter(
    encounter_request: CreateEncounterRequest,
    current_user: str = Depends(get_current_user),
    encounter_repository: EncounterRepository = Depends(get_encounter_repository),
) -> GetEncounterResponse:
    #
    logger.info(f"create_encounter: {encounter_request}")

    encounter = encounter_repository.add_encounter(
        encounter_request.patient_id,
        encounter_request.provider_id,
        encounter_request.encounter_date,
        encounter_request.encounter_type,
        encounter_request.clinical_data,
        current_user,
    )
    return GetEncounterResponse.from_encounter(encounter)


@router.get("/encounters/{encounterId}")
def get_encounter(
    encounter_id: UUID = Path(alias="encounterId"),
    current_user: str = Depends(get_current_user),
    encounter_repository: EncounterRepository = Depends(get_encounter_repository),
) -> GetEncounterResponse:
    encounter = encounter_repository.get_encounter(encounter_id, user_id=current_user)
    return GetEncounterResponse.from_encounter(encounter)


class AccessType(Enum):
    READ = "read"
    WRITE = "write"


class AuditEventResponse(BaseModel):
    encounterId: UUID
    accessType: AccessType
    userId: str
    accessedOn: datetime


class EncounterQuery(BaseModel):
    start_date_time: Optional[datetime] = Field(None, alias="startDateTime")
    end_date_time: Optional[datetime] = Field(None, alias="endDateTime")

    class Config:
        populate_by_name = True  # allow internal snake_case names


@router.get("/audit/encounters")
def list_audit_events_for_encounters(
    q: EncounterQuery = Depends(),
    encounter_repository: EncounterRepository = Depends(get_encounter_repository),
) -> list[AuditEventResponse]:
    results = []
    for encounter in encounter_repository.list_encounters():
        write_event = AuditEventResponse(
            encounterId=encounter.encounter_id,
            accessType=AccessType.WRITE,
            userId=encounter.metadata.createdBy,
            accessedOn=encounter.metadata.createdAt,
        )
        if _matches_filter(write_event.accessedOn, q):
            results.append(write_event)

        for access in encounter.accesses:
            read_event = AuditEventResponse(
                encounterId=encounter.encounter_id,
                accessType=AccessType.READ,
                userId=access.accessedBy,
                accessedOn=access.accessedOn,
            )
            if _matches_filter(read_event.accessedOn, q):
                results.append(read_event)
    return results


def _matches_filter(accessed_on: datetime, query: EncounterQuery) -> bool:
    if query.start_date_time and accessed_on < query.start_date_time:
        return False
    if query.end_date_time and accessed_on > query.end_date_time:
        return False
    return True
