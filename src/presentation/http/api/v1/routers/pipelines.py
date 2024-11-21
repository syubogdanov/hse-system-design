from http import HTTPStatus
from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.domain.entities.order import Order
from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import Stage


TAG: Final[str] = "pipelines"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all() -> list[Pipeline]:
    """Получить список всех пайплайнов."""


@router.get("/{id}")
async def get(id_: Annotated[UUID, Path(alias="id")]) -> Pipeline:
    """Получить пайплайн по идентификатору."""


@router.get("/{id}/stages")
async def get_stages(id_: Annotated[UUID, Path(alias="id")]) -> list[Stage]:
    """Получить все этапы пайплайна."""


@router.post("/{id}/cancel")
async def cancel(id_: Annotated[UUID, Path(alias="id")]) -> None:
    """Отменить пайплайн."""


@router.post("/{id}/restart", status_code=HTTPStatus.ACCEPTED)
async def restart(id_: Annotated[UUID, Path(alias="id")]) -> UUID:
    """Перезапустить пайплайн."""


@router.post("/start", status_code=HTTPStatus.ACCEPTED)
async def start(order: Order) -> UUID:
    """Начать пайплайн."""