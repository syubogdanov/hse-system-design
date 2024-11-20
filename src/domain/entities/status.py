from enum import StrEnum, auto
from typing import Self


class Status(StrEnum):
    """Статус выполнения."""

    PENDING = auto()
    IN_PROGRESS = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CANCELED = auto()

    def is_final(self: Self) -> bool:
        """Проверить, что статус финальный."""
        return self in {Status.SUCCEEDED, Status.FAILED, Status.CANCELED}
