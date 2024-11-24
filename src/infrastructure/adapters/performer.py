from contextlib import AbstractAsyncContextManager
from typing import Self
from uuid import UUID

from src.domain.services.interfaces.performer import PerformerInterface


class PerformerAdapter(PerformerInterface):
    """Адаптер исполнителя."""

    async def is_busy(self: Self, performer_id: UUID) -> bool:
        """Получить пайплайн по идентификатору."""
        raise NotImplementedError

    def lock(self: Self, performer_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать назначение исполнителя на заказы."""
        raise NotImplementedError
