from uuid import UUID

from pydantic import BaseModel


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    source_address_id: UUID
    target_address_id: UUID
