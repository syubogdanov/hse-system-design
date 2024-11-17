from pydantic import BaseModel

from src.domain.entities.pipeline import PipelineName


class Trigger(BaseModel):
    """Сущность триггера."""

    pipeline: PipelineName
