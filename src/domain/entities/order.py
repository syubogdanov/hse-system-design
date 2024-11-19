from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.task import TaskName
from utils.datetime import utcnow


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    last_task: TaskName = TaskName.START
    updated_at: AwareDatetime = Field(default_factory=utcnow)
    created_at: AwareDatetime = Field(default_factory=utcnow)
