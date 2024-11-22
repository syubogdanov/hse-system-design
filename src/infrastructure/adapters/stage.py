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

    async def get(self: Self, stage_id: UUID) -> "Stage":
        """Получить этап по идентификатору."""
        raise NotImplementedError

    async def get_all(self: Self, *, pipeline_id: UUID | None = None) -> list["Stage"]:
        """Получить список всех этапов."""
        raise NotImplementedError

    async def get_latest(self: Self, pipeline_id: UUID) -> "Stage | None":
        """Получить последний запущенный этап."""
        raise NotImplementedError
