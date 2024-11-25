from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, NonNegativeFloat

from utils.datetime import utcnow


class Delivery(BaseModel):
    """Сущность доставки."""

    pipeline_id: UUID

    cost: NonNegativeFloat | None = None
    estimated_at: AwareDatetime | None = None

    performer_id: UUID | None = None
    assigned_at: AwareDatetime | None = None
    released_at: AwareDatetime | None = None

    model_config = ConfigDict(from_attributes=True)

    def assign(self: Self, performer_id: UUID) -> None:
        """Назначить исполнителя."""
        self.performer_id = performer_id
        self.assigned_at = utcnow()

    def release(self: Self) -> None:
        """Освободить исполнителя."""
        self.released_at = utcnow()

    def estimate(self: Self, cost: NonNegativeFloat) -> None:
        """Оценить стоимость заказа."""
        self.cost = cost
        self.estimated_at = utcnow()

    def is_assigned(self: Self) -> bool:
        """Проверить, что курьер назначен."""
        return self.performer_id is not None

    def is_estimated(self: Self) -> bool:
        """Проверить, что стоимость вычислена."""
        return self.cost is not None

    def is_ready(self: Self) -> bool:
        """Проверить, что данные по доставке готовы."""
        return self.is_assigned() and self.is_estimated()
