from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    BROKEN_ORDER = "The order of tasks is broken"
    RUNNER_NOT_FOUND = "The task's runner was not found"
    WRONG_TASK = "The wrong task was launched"
