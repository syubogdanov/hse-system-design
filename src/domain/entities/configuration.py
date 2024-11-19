from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from utils.datetime import utcnow


class Configuration(BaseModel):
    """Сущность конфигурации."""

    id: UUID
    fetched_at: AwareDatetime = Field(default_factory=utcnow)
