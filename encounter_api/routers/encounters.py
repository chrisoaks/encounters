from fastapi import APIRouter
from typing import Any, Dict
from uuid import uuid4
from datetime import datetime


from pydantic import BaseModel
from typing import Any
import json


router = APIRouter()


class CreateEncounterRequest(BaseModel):
    patient_id: str
    provider_id: str
    encounter_datetime: datetime

    clinical_data: dict[str, Any]


@router.post("/encounters", status_code=201)
def create_encounter(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {}
