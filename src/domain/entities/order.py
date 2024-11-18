from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.task import TaskName


class Order(BaseModel):
    """Сущность заказа."""

    id: UUID
    last_task: TaskName = TaskName.START
