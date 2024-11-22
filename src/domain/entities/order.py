from uuid import UUID

from pydantic import BaseModel


class OrderParameters(BaseModel):
    """Сущность параметров заказа."""

    id: UUID
    source_address: UUID
    target_address: UUID


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
