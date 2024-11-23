from typing import Final

from fastapi import APIRouter


TAG: Final[str] = "healthcheck"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/healthcheck")
async def healthcheck() -> None:
    """Проверить, что сервис активен."""
