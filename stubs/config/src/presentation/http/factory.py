from typing import Final

from fastapi import FastAPI

from src.container import CONTAINER
from src.presentation.http.api.v1 import factory


DOCS_URL: Final[str] = "/"


def create_app() -> FastAPI:
    """Фабрика `HTTP` API."""
    settings = CONTAINER.app_settings()

    app = FastAPI(title=settings.name, docs_url=DOCS_URL)

    v1 = factory.create_router()

    app.include_router(v1)

    return app
