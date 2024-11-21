from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.performer import Performer


class PerformerInterface(Protocol):
    """Интерфейс исполнителя."""

    @abstractmethod
    async def get(self: Self, performer_id: UUID) -> "Performer":
        """Получить исполнителя по идентфикатору."""

    @abstractmethod
    async def update_or_create(self: Self, performer: "Performer") -> None:
        """Обновить или сохранить исполнителя."""
