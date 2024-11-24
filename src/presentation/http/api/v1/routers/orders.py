from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path
from pydantic import NonNegativeFloat

from src.container import CONTAINER
from src.domain.entities.order import OrderParameters
from src.domain.entities.pipeline import Pipeline


TAG: Final[str] = "orders"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/register", status_code=HTTPStatus.ACCEPTED)
async def register(parameters: OrderParameters) -> None:
    """Зарегистрировать заказ и начать пайплайн."""
    adapter = CONTAINER.order_adapter()
    launcher = CONTAINER.pipeline_launcher()

    if not (order := await adapter.register(parameters)):
        detail = "The order has already been registered"
        raise HTTPException(HTTPStatus.CONFLICT, detail)

    await launcher.start_or_restart(order.id)


@router.get("/{id}/cost")
async def get_cost(order_id: Annotated[UUID, Path(alias="id")]) -> NonNegativeFloat:
    """Получить исполнителя заказа."""
    delivery_adapter = CONTAINER.delivery_adapter()
    pipeline_adapter = CONTAINER.pipeline_adapter()

    if not (pipeline := await pipeline_adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    if not pipeline.status.is_final():
        detail = "The pipeline is still running..."
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail)

    delivery = await delivery_adapter.get(pipeline.id)

    if delivery.cost is None:
        detail = "The cost has not been estimated"
        raise HTTPException(HTTPStatus.EXPECTATION_FAILED, detail)

    return delivery.cost


@router.get("/{id}/performer")
async def get_performer(order_id: Annotated[UUID, Path(alias="id")]) -> UUID:
    """Получить исполнителя заказа."""
    delivery_adapter = CONTAINER.delivery_adapter()
    pipeline_adapter = CONTAINER.pipeline_adapter()

    if not (pipeline := await pipeline_adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    if not pipeline.status.is_final():
        detail = "The pipeline is still running..."
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail)

    delivery = await delivery_adapter.get(pipeline.id)

    if not delivery.performer_id:
        detail = "No performers have been assigned"
        raise HTTPException(HTTPStatus.EXPECTATION_FAILED, detail)

    return delivery.performer_id


@router.get("/{id}/pipelines")
async def get_pipelines(order_id: Annotated[UUID, Path(alias="id")]) -> list[Pipeline]:
    """Получить список пайплайнов заказа."""
    order_adapter = CONTAINER.order_adapter()
    pipeline_adapter = CONTAINER.pipeline_adapter()

    if not await order_adapter.exists(order_id):
        detail = "The order was not found"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return await pipeline_adapter.get_all(order_id=order_id)


@router.get("/{id}/pipelines/latest")
async def get_latest_pipeline(order_id: Annotated[UUID, Path(alias="id")]) -> Pipeline:
    """Получить актуальный пайплайн."""
    adapter = CONTAINER.pipeline_adapter()

    if not (pipeline := await adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return pipeline


@router.post("/{id}/pipelines/latest/cancel")
async def cancel_latest_pipeline(order_id: Annotated[UUID, Path(alias="id")]) -> None:
    """Отменить пайплайн."""
    launcher = CONTAINER.pipeline_launcher()

    await launcher.cancel(order_id)


@router.post("/{id}/pipelines/latest/restart", status_code=HTTPStatus.ACCEPTED)
async def restart_latest_pipeline(order_id: Annotated[UUID, Path(alias="id")]) -> UUID:
    """Перезапустить пайплайн."""
    launcher = CONTAINER.pipeline_launcher()

    return await launcher.start_or_restart(order_id)

