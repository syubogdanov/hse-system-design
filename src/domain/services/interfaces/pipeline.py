from abc import abstractmethod
from datetime import timedelta
from typing import Protocol, Self
from uuid import UUID


class PipelineInterface(Protocol):
    """Интерфейс пайплайна."""

    @abstractmethod
    async def is_canceled(self: Self, pipeline_id: UUID) -> bool:
        """Проверить, отменен ли пайплайн."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить устаревшие пайпалайны из истории."""
