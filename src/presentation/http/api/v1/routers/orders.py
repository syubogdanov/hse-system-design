from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.domain.entities.order import Order
from src.domain.entities.performer import Performer


TAG: Final[str] = "orders"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all() -> list[Order]:
    """Получить список всех заказов."""


@router.get("/{id}")
async def get(id_: Annotated[UUID, Path(alias="id")]) -> Order:
    """Получить заказ по идентификатору."""


@router.get("/{id}/performer")
async def get_performer(id_: Annotated[UUID, Path(alias="id")]) -> Performer:
    """Получить исполнителя заказа."""
