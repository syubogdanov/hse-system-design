from uuid import UUID

from pydantic import AwareDatetime, BaseModel, NonNegativeFloat


class Config(BaseModel):
    """Сущность конфига."""

    id: UUID
    min_cost: NonNegativeFloat
    rubles_per_meter: NonNegativeFloat
    fetched_at: AwareDatetime
