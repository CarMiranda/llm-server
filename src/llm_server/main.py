import uvicorn
from fastapi import FastAPI

from llm_server.api import api_router
from llm_server.config import settings


def create_app():
    app = FastAPI()
    app.include_router(api_router)

    return app


def serve():
    app = create_app()
    uvicorn.run(app, host=settings.host, port=settings.port)
