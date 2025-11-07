from datetime import datetime
from uuid import UUID

from encounter_api.enums import EncounterType
from encounter_api.state import EncounterMetadata, AccessEvent, EncounterState
from encounter_api.types import SecretUUID, SecretJson


class EncounterException(Exception):
    pass


class EncounterRepository:
    def __init__(self) -> None:
        self.encounters: dict[UUID, EncounterState] = dict()

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
