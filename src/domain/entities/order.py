from uuid import UUID

from pydantic import BaseModel


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
