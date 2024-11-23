from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from utils.datetime import utcnow


class OrderParameters(BaseModel):
    """Сущность параметров заказа."""

    id: UUID
    source_address: UUID
    target_address: UUID


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    source_address: UUID
    target_address: UUID
    registered_at: AwareDatetime = Field(default_factory=utcnow)
