from uuid import UUID

from pydantic import AwareDatetime, BaseModel, NonNegativeFloat

from utils.typing import JSON


class Config(BaseModel):
    """Сущность конфига."""

    id: UUID
    min_cost: NonNegativeFloat
    rubles_per_meter: NonNegativeFloat
    fetched_at: AwareDatetime
    metadata: JSON | None = None
