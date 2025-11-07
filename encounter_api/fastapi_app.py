from fastapi import FastAPI
from .routers.encounters import router as encounters_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(encounters_router)
    return app
