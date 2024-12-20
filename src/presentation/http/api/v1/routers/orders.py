from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path

from src.container import CONTAINER
from src.domain.entities.delivery import Delivery
from src.domain.entities.order import Order, OrderParameters
from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import Stage


TAG: Final[str] = "orders"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/register", status_code=HTTPStatus.ACCEPTED)
async def register(parameters: OrderParameters) -> UUID:
    """Зарегистрировать заказ и начать пайплайн."""
    adapter = CONTAINER.order_adapter()
    launcher = CONTAINER.pipeline_launcher()

    if not (order := await adapter.register(parameters)):
        detail = "The order has already been registered"
        raise HTTPException(HTTPStatus.CONFLICT, detail)

    return await launcher.start_or_restart(order.id)


@router.get("/{id}")
async def get_order(order_id: Annotated[UUID, Path(alias="id")]) -> Order:
    """Получить информацию по заказу."""
    order_adapter = CONTAINER.order_adapter()

    return await order_adapter.get(order_id=order_id)


@router.get("/{id}/pipelines")
async def get_pipelines(order_id: Annotated[UUID, Path(alias="id")]) -> list[Pipeline]:
    """Получить список пайплайнов заказа."""
    order_adapter = CONTAINER.order_adapter()
    pipeline_adapter = CONTAINER.pipeline_adapter()

    if not await order_adapter.exists(order_id):
        detail = "The order was not found"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return await pipeline_adapter.get_all(order_id=order_id)


@router.get("/{id}/stages/latest")
async def get_latest_stage(order_id: Annotated[UUID, Path(alias="id")]) -> Stage:
    """Получить актуальный этап."""
    pipeline_adapter = CONTAINER.pipeline_adapter()
    stage_adapter = CONTAINER.stage_adapter()

    if not (pipeline := await pipeline_adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    if not (stage := await stage_adapter.get_latest(pipeline.id)):
        detail = "No stages have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return stage


@router.get("/{id}/pipelines/latest")
async def get_latest_pipeline(order_id: Annotated[UUID, Path(alias="id")]) -> Pipeline:
    """Получить актуальный пайплайн."""
    adapter = CONTAINER.pipeline_adapter()

    if not (pipeline := await adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    return pipeline


@router.get("/{id}/pipelines/latest/delivery")
async def get_delivery(order_id: Annotated[UUID, Path(alias="id")]) -> Delivery:
    """Получить информацию по доставке."""
    delivery_adapter = CONTAINER.delivery_adapter()
    pipeline_adapter = CONTAINER.pipeline_adapter()

    if not (pipeline := await pipeline_adapter.get_latest(order_id)):
        detail = "No pipelines have been launched yet"
        raise HTTPException(HTTPStatus.NOT_FOUND, detail)

    delivery =  await delivery_adapter.get(pipeline.id)

    if not delivery.is_ready():
        detail = "The delivery details are not ready yet"
        raise HTTPException(HTTPStatus.TOO_EARLY, detail)

    return delivery


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
