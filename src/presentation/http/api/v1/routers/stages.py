from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.domain.entities.stage import Stage


TAG: Final[str] = "stages"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all() -> list[Stage]:
    """Получить список всех этапов."""


@router.get("/{id}")
async def get(id_: Annotated[UUID, Path(alias="id")]) -> Stage:
    """Получить этап по идентификатору."""
