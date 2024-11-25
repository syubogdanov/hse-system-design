from typing import Final

from fastapi import FastAPI

from src.container import CONTAINER
from src.domain.services.exceptions import NotFoundError, PipelineError
from src.presentation.http.api.admin import factory as admin
from src.presentation.http.api.v1 import factory as v1
from src.presentation.http.handlers import on_not_found_error, on_pipeline_error


DOCS_URL: Final[str] = "/"


def create_app() -> FastAPI:
    """Фабрика `HTTP` API."""
    settings = CONTAINER.app_settings()

    app = FastAPI(title=settings.name, version=settings.version, docs_url=DOCS_URL)

    app.add_exception_handler(NotFoundError, on_not_found_error)
    app.add_exception_handler(PipelineError, on_pipeline_error)

    app.include_router(v1.create_router())
    app.include_router(admin.create_router())

    return app
