from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from utils.datetime import utcnow


class Assignment(BaseModel):
    """Сущность назначения."""

    order_id: UUID
    performer_id: UUID
    assigned_at: AwareDatetime = Field(default_factory=utcnow)
    released_at: AwareDatetime | None = None

    def release(self: Self) -> None:
        """Освободить исполнителя от заказа."""
        self.released_at = utcnow()
