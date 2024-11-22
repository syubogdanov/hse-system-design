from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.order import Order, OrderParameters


class OrderInterface(Protocol):
    """Интерфейс заказа."""

    @abstractmethod
    async def register(self: Self, parameters: "OrderParameters") -> "Order | None":
        """Зарегистрировать заказ."""
