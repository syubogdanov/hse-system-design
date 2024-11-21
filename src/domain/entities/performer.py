from uuid import UUID

from pydantic import BaseModel


class Performer(BaseModel):
    """Сущность исполнителя."""

    id: UUID
