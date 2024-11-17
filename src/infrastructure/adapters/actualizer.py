from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.actualizer import ActualizerInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class ActualizerAdapter(ActualizerInterface):
    """Адаптер актуализатора."""

    _logger: "Logger"

    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        raise NotImplementedError
