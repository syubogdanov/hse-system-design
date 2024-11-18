from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.order import Order


class OrderInterface(Protocol):
    """Интерфейс заказа."""

    @abstractmethod
    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""

    @abstractmethod
    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None, None]:
        """Заблокировать выполнение задач по заказу."""
