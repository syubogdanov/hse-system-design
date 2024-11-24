from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from utils.datetime import utcnow


class OrderParameters(BaseModel):
    """Сущность параметров заказа."""

    id: UUID
    source_address_id: UUID
    target_address_id: UUID


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    source_address_id: UUID
    target_address_id: UUID
    registered_at: AwareDatetime = Field(default_factory=utcnow)

    model_config = ConfigDict(from_attributes=True)
