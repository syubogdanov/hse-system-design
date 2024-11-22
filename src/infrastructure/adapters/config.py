from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class ConfigAdapter(Protocol):
    """Адаптер конфигурации."""

    _logger: "Logger"

    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        raise NotImplementedError
