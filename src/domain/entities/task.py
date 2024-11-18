from enum import StrEnum, auto
from typing import Self, assert_never


class TaskName(StrEnum):
    """Название задачи."""

    ASSIGN = auto()
    CANCEL = auto()
    ESTIMATE = auto()
    FINISH = auto()
    START = auto()

    def get_next(self: Self) -> "TaskName | None":
        """Получить следующую задачу."""
        if self == TaskName.START:
            return TaskName.ESTIMATE

        if self == TaskName.ESTIMATE:
            return TaskName.ASSIGN

        if self == TaskName.ASSIGN:
            return None

        if self == TaskName.CANCEL:
            return None

        if self == TaskName.FINISH:
            return None

        assert_never(self)

    def get_previous(self: Self) -> set["TaskName"]:
        """Получить предыдущие задачи."""
        if self == TaskName.START:
            return set()

        if self == TaskName.ESTIMATE:
            return {TaskName.START}

        if self == TaskName.ASSIGN:
            return {TaskName.ESTIMATE}

        if self == TaskName.CANCEL:
            return {TaskName.START, TaskName.ESTIMATE}

        if self == TaskName.FINISH:
            return {TaskName.ASSIGN}

        assert_never(self)
