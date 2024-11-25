from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path

from src.container import CONTAINER
from src.domain.entities.delivery import Delivery
from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import Stage


TAG: Final[str] = "pipelines"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{id}")
async def get(pipeline_id: Annotated[UUID, Path(alias="id")]) -> Pipeline:
    """Получить пайплайн по идентификатору."""
    adapter = CONTAINER.pipeline_adapter()

    return await adapter.get(pipeline_id)


@router.get("/{id}/stages")
async def get_stages(pipeline_id: Annotated[UUID, Path(alias="id")]) -> list[Stage]:
    """Получить все этапы пайплайна."""
    pipeline_adapter = CONTAINER.pipeline_adapter()
    stage_adapter = CONTAINER.stage_adapter()

    if not await pipeline_adapter.exists(pipeline_id):
        detail = "The pipeline was not found"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return await stage_adapter.get_all(pipeline_id=pipeline_id)


@router.get("/{id}/delivery")
async def get_delivery(pipeline_id: Annotated[UUID, Path(alias="id")]) -> Delivery:
    """Получить доставку, назначенную пайплайном."""
    adapter = CONTAINER.delivery_adapter()

    return await adapter.get(pipeline_id)
