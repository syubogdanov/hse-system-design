from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.order import Order


class OrderInterface(Protocol):
    """Интерфейс заказа."""

    @abstractmethod
    async def exists(self: Self, order_id: UUID) -> bool:
        """Проверить, существует ли заказ."""

    @abstractmethod
    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""

    @abstractmethod
    async def update_or_create(self: Self, order: "Order") -> None:
        """Обновить или сохранить сущность."""

    @abstractmethod
    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение задач по заказу."""
