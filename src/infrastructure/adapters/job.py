from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.job import JobInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.job import Job


@dataclass
class JobAdapter(JobInterface):
    """Адаптер заказа."""

    _logger: "Logger"

    async def exists(self: Self, id_: UUID) -> bool:
        """Проверить, существует ли работа."""
        raise NotImplementedError

    async def get(self: Self, id_: UUID) -> "Job":
        """Получить работу по идентификатору."""
        raise NotImplementedError

    async def update_or_create(self: Self, job: "Job") -> None:
        """Обновить или сохранить работу."""
        raise NotImplementedError

    @asynccontextmanager
    async def lock(self: Self, order_id: UUID) -> AsyncGenerator[None, None]:
        """Заблокировать выполнение задач по работе."""
        raise NotImplementedError

    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
        raise NotImplementedError
