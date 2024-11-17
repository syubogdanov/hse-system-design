from abc import abstractmethod
from datetime import timedelta
from typing import Protocol, Self


class CleanerInterface(Protocol):
    """Интерфейс очистителя."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
