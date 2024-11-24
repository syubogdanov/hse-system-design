from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.performer import Performer


class PerformerInterface(Protocol):
    """Интерфейс исполнителя."""

    @abstractmethod
    async def is_busy(self: Self, performer_id: UUID) -> bool:
        """Получить пайплайн по идентификатору."""

    @abstractmethod
    async def get_nearest(self: Self, zone_id: UUID) -> list["Performer"]:
        """Получить свободных исполнителей."""

    @abstractmethod
    def lock(self: Self, performer_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать назначение исполнителя на заказы."""
