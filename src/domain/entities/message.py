from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    STAGE_RUNNER_NOT_RUNNABLE = "The stage runner is not runnable"
    STAGE_RUNNER_NOT_FOUND = "The stage runner was not found"
