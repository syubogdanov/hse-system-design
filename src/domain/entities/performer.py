from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Performer(BaseModel):
    """Сущность исполнителя."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
