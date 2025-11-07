from enum import Enum


class EncounterType(Enum):
    initial_assessment = "initial_assessment"
    follow_up = "follow_up"
    treatment_session = "treatment_session"
