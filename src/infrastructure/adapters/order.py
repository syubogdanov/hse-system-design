from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.order import OrderInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.order import Order


@dataclass
class OrderAdapter(OrderInterface):
    """Адаптер заказа."""

    _logger: "Logger"

    async def exists(self: Self, order_id: UUID) -> bool:
        """Проверить, существует ли заказ."""
        raise NotImplementedError

    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""
        raise NotImplementedError

    async def update_or_create(self: Self, order: "Order") -> None:
        """Обновить или создать заказ."""
        raise NotImplementedError

    @asynccontextmanager
    async def lock(self: Self, order_id: UUID) -> AsyncGenerator[None, None]:
        """Заблокировать выполнение задач по заказу."""
        raise NotImplementedError
