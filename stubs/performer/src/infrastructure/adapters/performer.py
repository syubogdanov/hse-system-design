from dataclasses import dataclass
from secrets import randbelow
from typing import ClassVar, Self
from uuid import UUID, uuid4

from src.domain.entities.performer import Performer
from src.domain.services.interfaces.performer import PerformerInterface


@dataclass
class PerformerAdapter(PerformerInterface):
    """Адаптер исполнителя."""

    _max_performers: ClassVar[int] = 10

    async def get_nearest(self: Self, _zone_id: UUID) -> list["Performer"]:
        """Получить свободных исполнителей."""
        return [
            Performer(id=uuid4())
            for _ in range(randbelow(self._max_performers + 1))
        ]
