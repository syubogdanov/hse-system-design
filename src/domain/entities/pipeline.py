from enum import StrEnum, auto


class PipelineName(StrEnum):
    """Название пайплайна."""

    ASSIGNMENT = auto()
    CANCELLATION = auto()
    ESTIMATION = auto()
    RELEASE = auto()
