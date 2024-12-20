from uuid import UUID

from src.domain.entities.stage import StageName
from utils.kafka import Event


class Trigger(Event):
    """Сущность триггера."""

    pipeline_id: UUID
    stage_name: StageName
