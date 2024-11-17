from abc import abstractmethod
from typing import Protocol, Self


class ActualizerInterface(Protocol):
    """Интерфейс актуализатора."""

    @abstractmethod
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
