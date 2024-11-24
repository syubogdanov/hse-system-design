from typing import Self

from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    """Сущность события."""

    def __bytes__(self: Self) -> bytes:
        """Отобразить в `bytes`."""
        return self.model_dump_json().encode()

    @classmethod
    def from_bytes(cls: type[Self], data: bytes) -> Self:
        """Сконструировать из `bytes`."""
        return cls.model_validate_json(data)

    model_config = ConfigDict(from_attributes=True)
