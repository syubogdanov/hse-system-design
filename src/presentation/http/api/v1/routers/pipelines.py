from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.container import CONTAINER
from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import Stage


TAG: Final[str] = "pipelines"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all(order_id: UUID | None = None) -> list[Pipeline]:
    """Получить список всех пайплайнов."""
    adapter = CONTAINER.pipeline_adapter()

    return await adapter.get_all(order_id=order_id)


@router.get("/{id}")
async def get(pipeline_id: Annotated[UUID, Path(alias="id")]) -> Pipeline:
    """Получить пайплайн по идентификатору."""
    adapter = CONTAINER.pipeline_adapter()

    return await adapter.get(pipeline_id)


@router.get("/{id}/stages")
async def get_stages(pipeline_id: Annotated[UUID, Path(alias="id")]) -> list[Stage]:
    """Получить все этапы пайплайна."""
    adapter = CONTAINER.stage_adapter()

    return await adapter.get_all(pipeline_id=pipeline_id)
