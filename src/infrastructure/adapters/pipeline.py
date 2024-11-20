from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.pipeline import PipelineInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"

    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить устаревшие пайпалайны из истории."""
        raise NotImplementedError
