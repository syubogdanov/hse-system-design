from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.trigger import TriggerInterface


if TYPE_CHECKING:
    from src.domain.entities.trigger import Trigger


class TriggerAdapter(TriggerInterface):
    """Адаптер триггер-событий."""

    async def push(self: Self, trigger: "Trigger") -> None:
        """Отправить триггер на выполнение."""
        raise NotImplementedError
