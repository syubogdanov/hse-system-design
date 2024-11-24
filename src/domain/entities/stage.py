from enum import StrEnum, auto
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class StageName(StrEnum):
    """Название этапа."""

    START_PIPELINE = auto()
    ESTIMATE_COST = auto()
    ASSIGN_PERFORMER = auto()
    PERFORM_DELIVERY = auto()
    RELEASE_PERFORMER = auto()

    def get_next(self: Self) -> "StageName | None":
        """Получить название следующего этапа."""
        next_stages = {
            StageName.START_PIPELINE: StageName.ESTIMATE_COST,
            StageName.ESTIMATE_COST: StageName.ASSIGN_PERFORMER,
            StageName.ASSIGN_PERFORMER: StageName.PERFORM_DELIVERY,
            StageName.PERFORM_DELIVERY: StageName.RELEASE_PERFORMER,
        }
        return next_stages.get(self)

    def is_cancelable(self: Self) -> bool:
        """Проверить, разрешена ли отмена этапа."""
        return self in {StageName.START_PIPELINE, StageName.ESTIMATE_COST}

    @staticmethod
    def first() -> "StageName":
        """Получить название первого этапа."""
        return StageName.START_PIPELINE


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

    model_config = ConfigDict(from_attributes=True)

    def start(self: Self) -> None:
        """Запустить этап."""
        self.started_at = utcnow()

    def finish(self: Self, status: Status, message: str | None = None) -> None:
        """Завершить этап."""
        self.status = status
        self.message = message
        self.finished_at = utcnow()
