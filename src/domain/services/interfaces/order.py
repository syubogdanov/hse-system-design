from abc import abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.order import Order, OrderParameters


class OrderInterface(Protocol):
    """Интерфейс заказа."""

    @abstractmethod
    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""

    @abstractmethod
    async def register(self: Self, parameters: "OrderParameters") -> "Order | None":
        """Зарегистрировать заказ."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
