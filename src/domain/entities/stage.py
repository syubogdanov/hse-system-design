from enum import StrEnum, auto
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class StageName(StrEnum):
    """Название этапа.

    Примечания:
        * Порядок объявления влияет на очередность этапов.
    """

    START_PIPELINE = auto()
    ESTIMATE_PRICE = auto()
    ASSIGN_PERFORMER = auto()
    PERFORM_ORDER = auto()
    RELEASE_PERFORMER = auto()

    def get_next(self: Self) -> "StageName":
        """Получить название следующего этапа."""
        stages = list(StageName)
        index = stages.index(self) + 1
        return StageName(stages[index]) if index < len(stages) else None

    def is_cancelable(self: Self) -> bool:
        """Проверить, разрешена ли отмена этапа."""
        return self in {StageName.START_PIPELINE, StageName.ESTIMATE_PRICE}

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
    created_at: AwareDatetime = Field(default_factory=utcnow)
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
