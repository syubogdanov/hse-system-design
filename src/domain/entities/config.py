from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, NonNegativeFloat

from utils.datetime import utcnow


class Config(BaseModel):
    """Сущность конфига."""

    id: UUID
    min_cost: NonNegativeFloat
    rubles_per_meter: NonNegativeFloat
    fetched_at: AwareDatetime = Field(default_factory=utcnow)

    model_config = ConfigDict(from_attributes=True)
