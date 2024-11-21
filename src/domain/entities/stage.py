from enum import StrEnum, auto
from typing import Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

from src.domain.entities.status import Status
from utils.datetime import utcnow


class StageName(StrEnum):
    """Название этапа."""

    START_PIPELINE = auto()
    ESTIMATE_PRICE = auto()
    ASSIGN_PERFORMER = auto()
    PERFORM_ORDER = auto()
    RELEASE_PERFORMER = auto()

    def get_next(self: Self) -> "StageName | None":
        """Получить название следующего этапа."""
        next_stages = {
            StageName.START_PIPELINE: StageName.ESTIMATE_PRICE,
            StageName.ESTIMATE_PRICE: StageName.ASSIGN_PERFORMER,
            StageName.ASSIGN_PERFORMER: StageName.PERFORM_ORDER,
            StageName.PERFORM_ORDER: StageName.RELEASE_PERFORMER,
        }
        return next_stages.get(self)

    def is_asynchronous(self: Self) -> bool:
        """Проверить, является ли этап асинхронным."""
        return self in {StageName.PERFORM_ORDER}

    def is_cancelable(self: Self) -> bool:
        """Проверить, разрешено ли отменять этап."""
        return self in {StageName.START_PIPELINE, StageName.ESTIMATE_PRICE}

    @classmethod
    def first(cls: type[Self]) -> Self:
        """Получить название первого этапа."""
        return cls.START_PIPELINE


class Stage(BaseModel):
    """Сущность этапа."""

    id: UUID
    pipeline_id: UUID
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

    def autofinish(self: Self, status: Status, message: str | None = None) -> None:
        """Начать и сразу же завершить выполнение."""
        self.start()
        self.finish(status, message)
