from abc import abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.order import Order


class OrderInterface(Protocol):
    """Интерфейс заказа."""

    @abstractmethod
    async def update_or_create(self: Self, order: "Order") -> None:
        """Обновить или сохранить заказ."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить заказы старше порогового значения."""
