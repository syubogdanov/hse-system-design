from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.configuration import Configuration


class ConfigurationInterface(Protocol):
    """Интерфейс конфигурации."""

    @abstractmethod
    async def get(self: Self) -> "Configuration | None":
        """Получить конфигурацию."""

    @abstractmethod
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
