from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.configuration import ConfigurationInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.configuration import Configuration


@dataclass
class ConfigurationAdapter(ConfigurationInterface):
    """Адаптер конфигурации."""

    _logger: "Logger"

    async def get(self: Self) -> "Configuration | None":
        """Получить конфигурацию."""
        raise NotImplementedError

    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        raise NotImplementedError
