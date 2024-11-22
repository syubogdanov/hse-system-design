from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.trigger import TriggerInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger


@dataclass
class TriggerAdapter(TriggerInterface):
    """Интерфейс триггер-событий."""

    _logger: "Logger"

    async def push(self: Self, trigger: "Trigger") -> None:
        """Отправить триггер на выполнение."""
        raise NotImplementedError
