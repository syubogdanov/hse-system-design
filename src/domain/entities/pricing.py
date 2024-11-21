from uuid import UUID

from pydantic import BaseModel


class Pricing(BaseModel):
    """Сущность ценообразования."""

    order_id: UUID
    config_id: UUID
