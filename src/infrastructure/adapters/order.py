from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.order import OrderInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.order import Order, OrderParameters


@dataclass
class OrderAdapter(OrderInterface):
    """Адаптер заказа."""

    _logger: "Logger"

    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""
        raise NotImplementedError

    async def register(self: Self, parameters: "OrderParameters") -> "Order | None":
        """Зарегистрировать заказ."""
        raise NotImplementedError

    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
        raise NotImplementedError
