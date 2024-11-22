from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.trigger import Trigger


class TriggerInterface(Protocol):
    """Интерфейс триггер-событий."""

    @abstractmethod
    async def push(self: Self, trigger: "Trigger") -> None:
        """Отправить триггер на выполнение."""
