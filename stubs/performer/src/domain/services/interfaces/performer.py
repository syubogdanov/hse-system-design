from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.performer import Performer


class PerformerInterface(Protocol):
    """Интерфейс исполнителя."""

    @abstractmethod
    async def get_nearest(self: Self, zone_id: UUID) -> list["Performer"]:
        """Получить свободных исполнителей."""
