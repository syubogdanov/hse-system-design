from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.order import OrderInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.order import Order, OrderParameters


@dataclass
class OrderAdapter(OrderInterface):
    """Адаптер заказа."""

    _logger: "Logger"

    async def register(self: Self, parameters: "OrderParameters") -> "Order | None":
        """Зарегистрировать заказ."""
        raise NotImplementedError
