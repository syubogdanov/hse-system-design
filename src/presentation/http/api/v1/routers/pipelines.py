from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path

from src.container import CONTAINER
from src.domain.entities.order import OrderParameters
from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import Stage


TAG: Final[str] = "pipelines"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all() -> list[Pipeline]:
    """Получить список всех пайплайнов."""
    adapter = CONTAINER.pipeline_adapter()

    return await adapter.get_all()


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


@router.post("/{id}/cancel")
async def cancel(pipeline_id: Annotated[UUID, Path(alias="id")]) -> None:
    """Отменить пайплайн."""
    adapter = CONTAINER.pipeline_adapter()
    launcher = CONTAINER.pipeline_launcher()

    pipeline = await adapter.get(pipeline_id)
    await launcher.cancel(pipeline.order_id)


@router.post("/{id}/restart", status_code=HTTPStatus.ACCEPTED)
async def restart(pipeline_id: Annotated[UUID, Path(alias="id")]) -> UUID:
    """Перезапустить пайплайн."""
    adapter = CONTAINER.pipeline_adapter()
    launcher = CONTAINER.pipeline_launcher()

    pipeline = await adapter.get(pipeline_id)
    return await launcher.start(pipeline.order_id)


@router.post("/start", status_code=HTTPStatus.ACCEPTED)
async def start(parameters: OrderParameters) -> UUID:
    """Начать пайплайн."""
    adapter = CONTAINER.order_adapter()
    launcher = CONTAINER.pipeline_launcher()

    if not (order := await adapter.register(parameters)):
        detail = "The order has already been registered"
        raise HTTPException(HTTPStatus.CONFLICT, detail)

    return await launcher.start(order.id)
