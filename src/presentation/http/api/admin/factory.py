from typing import Final

from fastapi import APIRouter

from src.presentation.http.api.admin.routers import result


PREFIX: Final[str] = "/admin"


def create_router() -> APIRouter:
    """Фабрика роутера `/admin`."""
    router = APIRouter(prefix=PREFIX)

    router.include_router(result.router)

    return router
