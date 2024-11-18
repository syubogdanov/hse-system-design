from typing import Self

from pydantic import BaseModel

from src.domain.entities.pipeline import PipelineName


class Trigger(BaseModel):
    """Сущность триггера."""

    pipeline: PipelineName

    def to_bytes(self: Self) -> bytes:
        """Отобразить в `bytes`."""
        return self.model_dump_json().encode()

    @classmethod
    def from_bytes(cls: type[Self], data: bytes) -> Self:
        """Сконструировать из `bytes`."""
        return cls.model_validate_json(data)
