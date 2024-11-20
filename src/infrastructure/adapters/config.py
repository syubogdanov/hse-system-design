from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.config import ConfigInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class ConfigAdapter(ConfigInterface):
    """Адаптер конфигурации."""

    _logger: "Logger"

    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        raise NotImplementedError
