from typing import Final

from fastapi import FastAPI

from src.domain.services.exceptions import NotFoundError, PipelineError, StageError
from src.presentation.http.api.v1 import factory
from src.presentation.http.handlers import on_not_found_error, on_pipeline_error, on_stage_error


TITLE: Final[str] = "Performix API"
DOCS_URL: Final[str] = "/"


def create_app() -> FastAPI:
    """Фабрика `HTTP` API."""
    app = FastAPI(title=TITLE, docs_url=DOCS_URL)

    v1 = factory.create_router()

    app.add_exception_handler(NotFoundError, on_not_found_error)
    app.add_exception_handler(PipelineError, on_pipeline_error)
    app.add_exception_handler(StageError, on_stage_error)

    app.include_router(v1)

    return app
