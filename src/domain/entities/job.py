from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.task import TaskName
from utils.datetime import utcnow


class Job(BaseModel):
    """Сущность работы."""

    id: UUID
    task: TaskName
    configuration_id: UUID | None = None
    updated_at: AwareDatetime = Field(default_factory=utcnow)
    created_at: AwareDatetime = Field(default_factory=utcnow)

    def complete_task(self: Self, task: TaskName) -> None:
        """Завершить задачу."""
        self.task = task
        self.updated_at = utcnow()
