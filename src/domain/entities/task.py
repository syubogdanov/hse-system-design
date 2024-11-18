from enum import StrEnum, auto


class TaskName(StrEnum):
    """Название задачи."""

    ASSIGN = auto()
    CANCEL = auto()
    ESTIMATE = auto()
    FINISH = auto()
    START = auto()
