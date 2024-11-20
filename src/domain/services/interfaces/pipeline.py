from abc import abstractmethod
from datetime import timedelta
from typing import Protocol, Self


class PipelineInterface(Protocol):
    """Интерфейс пайплайна."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Удалить устаревшие пайпалайны из истории."""
