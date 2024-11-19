from pydantic import AwareDatetime, BaseModel, Field

from utils.datetime import utcnow


class Pricing(BaseModel):
    """Сущность ценообразования."""

    estimated_at: AwareDatetime = Field(default_factory=utcnow)
