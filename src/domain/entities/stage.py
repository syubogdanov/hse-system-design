from enum import StrEnum, auto
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class StageName(StrEnum):
    """Название этапа.

    Примечания:
        * Порядок объявления влияет на порядок выполнения.
    """

    START = auto()
    ESTIMATE = auto()
    ASSIGN = auto()
    RELEASE = auto()

    def is_schedulable(self: Self) -> bool:
        """Проверить, планируется ли этап автоматически."""
        return self not in {StageName.RELEASE}

    def get_next(self: Self) -> "StageName | None":
        """Получить название следующего этапа."""
        stages = list(StageName)
        index = stages.index(self) + 1
        return StageName(stages[index]) if index < len(stages) else None

    def get_previous(self: Self) -> "StageName | None":
        """Получить название предыдущего этапа."""
        stages = list(StageName)
        index = stages.index(self) - 1
        return StageName(stages[index]) if index > 0 else None


class Stage(BaseModel):
    """Сущность этапа."""

    id: UUID
    job_id: UUID
    name: StageName
    status: Status = Status.PENDING
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
