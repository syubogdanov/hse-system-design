from uuid import UUID

from src.domain.entities.status import Status
from utils.kafka import Event
from utils.typing import JSON


class StageResult(Event):
    """Сущность результата."""

    stage_id: UUID
    status: Status
    message: str | None = None
    metadata: JSON | None = None
