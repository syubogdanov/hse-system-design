from enum import StrEnum, auto
from typing import Self
from uuid import UUID

from pydantic import BaseModel


class OrderStatus(StrEnum):
    """Статус заказа."""

    CANCELED = auto()
    FINISHED = auto()

    def is_final(self: Self) -> bool:
        """Проверить, что статус финальный."""
        return self in {OrderStatus.CANCELED, OrderStatus.FINISHED}


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    status: OrderStatus
