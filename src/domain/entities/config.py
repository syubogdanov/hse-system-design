from uuid import UUID

from pydantic import AwareDatetime, BaseModel


class Config(BaseModel):
    """Сущность конфига."""

    id: UUID
    fetched_at: AwareDatetime
