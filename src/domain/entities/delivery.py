from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, NonNegativeFloat

from utils.datetime import utcnow


class Delivery(BaseModel):
    """Сущность доставки."""

    pipeline_id: UUID

    price: NonNegativeFloat | None = None
    estimated_at: AwareDatetime | None = None

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

    def estimate(self: Self, price: NonNegativeFloat) -> None:
        """Оценить стоимость заказа."""
        self.price = price
        self.estimated_at = utcnow()
