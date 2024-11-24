from uuid import UUID

from pydantic import BaseModel


class Zone(BaseModel):
    """Сущность области."""

    id: UUID
