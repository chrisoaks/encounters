import json
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from encounter_api.dependencies import (
    get_encounter_repository,
    EncounterRepository,
    EncounterState, get_current_user,
)
from encounter_api.enums import EncounterType

router = APIRouter()


class SecretJson:
    __slots__ = ("_value",)

    def __init__(self, value: Any):
        self._value = value

    def get_secret_value(self) -> Any:
        return self._value

    def __repr__(self):
        return "SecretJson('**********')"

    def __str__(self):
        return "**********"

    def __eq__(self, other):
        if isinstance(other, SecretJson):
            return self._value == other._value
        return False

    def json(self) -> str:
        return json.dumps(self._value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        # validator: any JSON → SecretJson
        def validate(value: Any) -> "SecretJson":
            if isinstance(value, SecretJson):
                return value
            return cls(value)

        # serializer: SecretJson → underlying JSON value
        def serialize(value: "SecretJson") -> Any:
            return value.get_secret_value()

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                when_used="json",
            ),
        )


class CreateEncounterRequest(BaseModel):
    patientId: UUID
    providerId: UUID
    encounterDate: datetime
    encounterType: EncounterType
    clinicalData: SecretJson


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
    encounter = encounter_repository.add_encounter(
        encounter_request.patientId,
        encounter_request.providerId,
        encounter_request.encounterDate,
        encounter_request.encounterType,
        encounter_request.clinicalData,
        current_user,
    )
    return GetEncounterResponse.from_encounter(encounter)


@router.get("/encounters/{encounterId}")
def get_encounter(
    encounterId: UUID,
    current_user: str = Depends(get_current_user),
    encounter_repository: EncounterRepository = Depends(get_encounter_repository),
) -> GetEncounterResponse:
    encounter = encounter_repository.get_encounter(encounterId)
    return GetEncounterResponse.from_encounter(encounter)


@router.get("/audit/encounters")
def list_audit_events_for_encounters(
    startDateTime: datetime, endDateTime: datetime
) -> list[GetEncounterResponse]:
    return []
