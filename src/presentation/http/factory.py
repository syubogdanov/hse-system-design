from typing import Final

from fastapi import FastAPI

from src.presentation.http.api.v1 import factory


TITLE: Final[str] = "HTTP API"
DOCS_URL: Final[str] = "/"


def create_app() -> FastAPI:
    """Фабрика `HTTP` API."""
    app = FastAPI(title=TITLE, docs_url=DOCS_URL)

    v1 = factory.create_router()

    app.include_router(v1)

    return app
