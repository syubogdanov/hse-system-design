from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.order import OrderInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.order import Order


@dataclass
class OrderAdapter(OrderInterface):
    """Адаптер заказа."""

    _logger: "Logger"

    async def update_or_create(self: Self, order: "Order") -> None:
        """Обновить или сохранить заказ."""
        raise NotImplementedError

    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить заказы, которые старше порогового значения."""
        raise NotImplementedError
