from abc import abstractmethod
from typing import Protocol, Self


class ConfigurationInterface(Protocol):
    """Интерфейс конфигурации."""

    @abstractmethod
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
