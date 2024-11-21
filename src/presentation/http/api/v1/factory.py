from typing import Final

from fastapi import APIRouter

from src.presentation.http.api.v1.routers import orders, performers, pipelines, stages


PREFIX: Final[str] = "/api/v1"


def create_router() -> APIRouter:
    """Фабрика роутера `/api/v1`."""
    router = APIRouter(prefix=PREFIX)

    router.include_router(pipelines.router)
    router.include_router(stages.router)
    router.include_router(orders.router)
    router.include_router(performers.router)

    return router
