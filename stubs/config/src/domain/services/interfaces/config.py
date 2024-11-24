from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.config import Config


class ConfigInterface(Protocol):
    """Интерфейс конфигурации."""

    @abstractmethod
    async def get(self: Self) -> "Config":
        """Получить конфигурацию."""