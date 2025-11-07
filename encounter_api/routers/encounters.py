from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from encounter_api.dependencies import get_encounter_repository, EncounterRepository, EncounterState
from encounter_api.enums import EncounterType

router = APIRouter()

class CreateEncounterRequest(BaseModel):
    patientId: UUID
    providerId: UUID
    encounterDate: datetime
    encounterType: EncounterType
    clinicalData: dict[str, Any]


class EncounterMetadata(BaseModel):
    createdAt: datetime
    updatedAt: datetime
    createdBy: str


class GetEncounterResponse(BaseModel):
    encounterId: UUID
    patientId: UUID
    providerId: UUID
    encounterDate: datetime
    encounterType: EncounterType
    clinicalData: dict[str, Any]
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
                createdBy=encounter.metadata.createdBy
            )
        )




@router.post("/encounters", status_code=201)
def create_encounter(encounter_request: CreateEncounterRequest, encounter_repository: EncounterRepository = Depends(get_encounter_repository)) -> GetEncounterResponse:
    encounter = encounter_repository.add_encounter(
        encounter_request.patientId,
        encounter_request.providerId,
        encounter_request.encounterDate,
        encounter_request.encounterType,
        encounter_request.clinicalData,

        "test_user" # TODO, fix
    )
    return GetEncounterResponse.from_encounter(encounter)


@router.get("/encounters/{encounterId}")
def get_encounter(encounterId: UUID, encounter_repository: EncounterRepository = Depends(get_encounter_repository)) -> GetEncounterResponse:
    encounter = encounter_repository.get_encounter(encounterId)
    return GetEncounterResponse.from_encounter(encounter)


@router.get("/audit/encounters")
def list_audit_events_for_encounters(startDateTime: datetime, endDateTime: datetime) -> list[GetEncounterResponse]:
    return []
