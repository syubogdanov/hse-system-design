from typing import Self
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.stage import StageName


class Trigger(BaseModel):
    """Сущность триггера."""

    pipeline_id: UUID
    stage_name: StageName

    def __bytes__(self: Self) -> bytes:
        """Отобразить в `bytes`."""
        return self.model_dump_json().encode()

    @classmethod
    def from_bytes(cls: type[Self], data: bytes) -> Self:
        """Сконструировать из `bytes`."""
        return cls.model_validate_json(data)
