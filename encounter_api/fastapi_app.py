from fastapi import FastAPI

from .repository import EncounterRepository
from .encounters import router as encounters_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.state.encounter_repository = EncounterRepository()
    app.include_router(encounters_router)
    return app
