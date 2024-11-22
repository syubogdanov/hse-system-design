from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.container import CONTAINER


TAG: Final[str] = "orders"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/{id}/pipeline/cancel")
async def cancel(order_id: Annotated[UUID, Path(alias="id")]) -> None:
    """Отменить пайплайн."""
    launcher = CONTAINER.pipeline_launcher()

    await launcher.cancel(order_id)


@router.post("/{id}/pipeline/restart", status_code=HTTPStatus.ACCEPTED)
async def restart(order_id: Annotated[UUID, Path(alias="id")]) -> UUID:
    """Перезапустить пайплайн."""
    launcher = CONTAINER.pipeline_launcher()

    return await launcher.start(order_id)
