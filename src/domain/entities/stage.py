from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel

from src.domain.entities.status import Status
from utils.datetime import utcnow


class StageName(StrEnum):
    """Название этапа."""

    def get_next(self: Self) -> "StageName":
        """Получить название следующего этапа."""
        raise NotImplementedError

    @staticmethod
    def first() -> "StageName":
        """Получить название первого этапа."""
        raise NotImplementedError


class Stage(BaseModel):
    """Сущность этапа."""

    id: UUID
    pipeline_id: UUID
    name: StageName
    status: Status = Status.PENDING
    message: str | None = None
    started_at: AwareDatetime | None = None
    finished_at: AwareDatetime | None = None

    def start(self: Self) -> None:
        """Запустить этап."""
        self.started_at = utcnow()

    def finish(self: Self, status: Status, message: str | None = None) -> None:
        """Завершить этап."""
        self.status = status
        self.message = message
        self.finished_at = utcnow()
