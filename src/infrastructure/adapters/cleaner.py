from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.cleaner import CleanerInterface


if TYPE_CHECKING:
    from logging import Logger


@dataclass
class CleanerAdapter(CleanerInterface):
    """Адаптер очистителя."""

    _logger: "Logger"

    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
        raise NotImplementedError
