from typing import Final

from fastapi import APIRouter

from src.presentation.http.api.v1.routers import address, healthcheck, math


PREFIX: Final[str] = "/api/v1"


def create_router() -> APIRouter:
    """Фабрика роутера `/api/v1`."""
    router = APIRouter(prefix=PREFIX)

    router.include_router(healthcheck.router)
    router.include_router(address.router)
    router.include_router(math.router)

    return router
