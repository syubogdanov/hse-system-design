from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self
from uuid import UUID

from conditional_cache import lru_cache

from src.domain.services.interfaces.pipeline import PipelineInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"

    @lru_cache(condition=lambda is_canceled: is_canceled is True)
    async def is_canceled(self: Self, pipeline_id: UUID) -> bool:
        """Проверить, отменен ли пайплайн.

        Примечания:
            * Положительные ответы кэшируются.
        """
        raise NotImplementedError

    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить устаревшие пайпалайны из истории."""
        raise NotImplementedError
