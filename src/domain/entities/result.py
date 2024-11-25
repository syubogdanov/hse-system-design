from typing import Self
from uuid import UUID

from pydantic import field_validator

from src.domain.entities.status import Status
from utils.kafka import Event


class Result(Event):
    """Сущность результата."""

    stage_id: UUID
    status: Status
    message: str | None = None

    @field_validator("status")
    @classmethod
    def ensure_status(cls: type[Self], status: Status) -> Status:
        """Проверить, что статус финальный."""
        if not status.is_final():
            detail = "The status is not final"
            raise ValueError(detail)
        return status
