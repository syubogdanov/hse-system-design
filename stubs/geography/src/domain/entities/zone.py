from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Zone(BaseModel):
    """Сущность области."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
