from abc import abstractmethod
from typing import Protocol, Self


class ConfigInterface(Protocol):
    """Интерфейс конфигурации."""

    @abstractmethod
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
