from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class Pipeline(BaseModel):
    """Сущность пайплайна."""

    id: UUID
    order_id: UUID
    status: Status = Status.PENDING
    message: str | None = None
    created_at: AwareDatetime = Field(default_factory=utcnow)
    started_at: AwareDatetime | None = None
    finished_at: AwareDatetime | None = None

    model_config = ConfigDict(from_attributes=True)

    def is_restartable(self: Self) -> bool:
        """Проверить, может ли пайплайн быть перезапущен."""
        return self.status in {Status.CANCELED, Status.FAILED}

    def start(self: Self) -> None:
        """Запустить этап."""
        self.status = Status.IN_PROGRESS
        self.started_at = utcnow()

    def finish(self: Self, status: Status, message: str | None = None) -> None:
        """Завершить этап."""
        self.status = status
        self.message = message
        self.finished_at = utcnow()
