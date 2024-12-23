from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.container import CONTAINER
from src.domain.entities.stage import Stage


TAG: Final[str] = "stages"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{id}")
async def get(stage_id: Annotated[UUID, Path(alias="id")]) -> Stage:
    """Получить этап по идентификатору."""
    adapter = CONTAINER.stage_adapter()

    return await adapter.get(stage_id)
