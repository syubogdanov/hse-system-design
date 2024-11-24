from uuid import UUID

from src.domain.entities.status import Status
from utils.kafka import Event


class Result(Event):
    """Сущность результата."""

    stage_id: UUID
    status: Status
    message: str | None = None
