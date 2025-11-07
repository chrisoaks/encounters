from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from encounter_api.enums import EncounterType
from encounter_api.types import SecretUUID, SecretJson


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
