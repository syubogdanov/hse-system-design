from enum import StrEnum, auto


class PipelineName(StrEnum):
    """Название пайплайна."""

    ASSIGN = auto()
    CANCEL = auto()
    ESTIMATE = auto()
    FINISH = auto()
    START = auto()
