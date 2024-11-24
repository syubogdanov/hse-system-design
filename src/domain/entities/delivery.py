from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel

from utils.datetime import utcnow


class Delivery(BaseModel):
    """Сущность доставки."""

    pipeline_id: UUID

    performer_id: UUID | None = None
    assigned_at: AwareDatetime | None = None
    released_at: AwareDatetime | None = None

    def assign(self: Self, performer_id: UUID) -> None:
        """Назначить исполнителя."""
        self.performer_id = performer_id
        self.assigned_at = utcnow()

    def release(self: Self) -> None:
        """Освободить исполнителя."""
        self.released_at = utcnow()

    def clear(self: Self) -> None:
        """Очистить сущность от данных."""
        self.performer_id = None
        self.assigned_at = None
        self.released_at = None
