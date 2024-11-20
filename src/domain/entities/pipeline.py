from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class Pipeline(BaseModel):
    """Сущность пайплайна."""

    id: UUID
    order_id: UUID
    status: Status = Status.PENDING
    message: str | None = None
    restartable: bool = False
    created_at: AwareDatetime = Field(default_factory=utcnow)
    started_at: AwareDatetime | None = None
    finished_at: AwareDatetime | None = None

    def start(self: Self) -> None:
        """Начать выполнение."""
        self.status = Status.IN_PROGRESS
        self.started_at = utcnow()

    def finish(self: Self, status: Status, message: str | None = None) -> None:
        """Отменить выполнение."""
        self.status = status
        self.message = message
        self.finished_at = utcnow()
