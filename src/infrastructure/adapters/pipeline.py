from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.pipeline import PipelineInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"

    async def is_canceled(self: Self, pipeline_id: UUID) -> bool:
        """Проверить, отменен ли пайплайн."""
        raise NotImplementedError

    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить устаревшие пайпалайны из истории."""
        raise NotImplementedError
