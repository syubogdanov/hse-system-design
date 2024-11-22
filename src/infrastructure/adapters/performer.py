from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.performer import PerformerInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.performer import Performer


@dataclass
class PerformerAdapter(PerformerInterface):
    """Адаптер исполнителя."""

    _logger: "Logger"

    async def get(self: Self, performer_id: UUID) -> "Performer":
        """Получить исполнителя по идентфикатору."""
        raise NotImplementedError

    async def get_all(self: Self) -> list["Performer"]:
        """Получить список всех исполнителей."""
        raise NotImplementedError

    async def update_or_create(self: Self, performer: "Performer") -> None:
        """Обновить или сохранить исполнителя."""
        raise NotImplementedError
