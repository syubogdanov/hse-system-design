from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.stage import StageInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage


@dataclass
class StageAdapter(StageInterface):
    """Адаптер этапа."""

    _logger: "Logger"

    async def update_or_create(self: Self, stage: "Stage") -> None:
        """Обновить или сохранить этап."""
        raise NotImplementedError

    async def get_last_started(self: Self, pipeline_id: UUID) -> "Stage":
        """Получить последний начатый этап."""
        raise NotImplementedError

    @asynccontextmanager
    def lock(self: Self, pipeline_id: UUID) -> AsyncGenerator[None, None]:
        """Заблокировать выполнение параллельных этапов."""
        raise NotImplementedError
