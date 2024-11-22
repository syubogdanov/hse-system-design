from typing import Final

from fastapi import FastAPI

from src.domain.services.exceptions import NotFoundError
from src.presentation.http.api.v1 import factory
from src.presentation.http.handlers import on_not_found


TITLE: Final[str] = "Performix API"
DOCS_URL: Final[str] = "/"


def create_app() -> FastAPI:
    """Фабрика `HTTP` API."""
    app = FastAPI(title=TITLE, docs_url=DOCS_URL)

    v1 = factory.create_router()

    app.add_exception_handler(NotFoundError, on_not_found)

    app.include_router(v1)

    return app
