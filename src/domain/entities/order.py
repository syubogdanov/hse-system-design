from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.task import TaskName
from utils.datetime import utcnow


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    last_task: TaskName
    updated_at: AwareDatetime = Field(default_factory=utcnow)
    created_at: AwareDatetime = Field(default_factory=utcnow)

    def complete(self: Self, task: TaskName) -> None:
        """Завершить задачу."""
        self.last_task = task
        self.updated_at = utcnow()
