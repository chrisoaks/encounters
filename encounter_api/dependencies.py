from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from starlette.requests import Request

from encounter_api.enums import EncounterType


@dataclass(kw_only=True)
class EncounterMetadata:
    createdAt: datetime = field(default_factory=datetime.utcnow)
    updatedAt: datetime = field(default_factory=datetime.utcnow)
    createdBy: str  # TODO, str correct?

@dataclass(kw_only=True)
class EncounterState:
    encounter_id: UUID = field(default_factory=uuid4)
    patient_id: UUID
    provider_id: UUID
    encounter_datetime: datetime
    encounter_type: EncounterType
    clinical_data: dict[str, Any]  # TODO restriction correct?
    metadata: EncounterMetadata


class EncounterRepository:
    def __init__(self):
        self.encounters: dict[UUID, EncounterState] = defaultdict()

    def add_encounter(
            self,
            patient_id: UUID,
            provider_id: UUID,
            encounter_datetime: datetime,
            encounter_type: EncounterType,
            clinical_data: dict[str, Any],
            created_by: str
    ) -> EncounterState:
        encounter = EncounterState(
            patient_id=patient_id,
            provider_id=provider_id,
            encounter_datetime=encounter_datetime,
            encounter_type=encounter_type,
            clinical_data=clinical_data,
            metadata=EncounterMetadata(createdBy=created_by)
        )
        self.encounters[encounter.encounter_id] = encounter
        return encounter
    def get_encounter(self, encounter_id: UUID) -> EncounterState:
        return self.encounters[encounter_id]


def get_encounter_repository(request: Request):
    return request.app.state.encounter_repository
