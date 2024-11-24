from typing import Final

from fastapi import APIRouter

from src.container import CONTAINER
from src.domain.entities.config import Config


TAG: Final[str] = "configs"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("latest")
async def get_latest() -> Config:
    """Получить актуальный конфиг."""
    adapter = CONTAINER.config_adapter()

    return await adapter.get()
