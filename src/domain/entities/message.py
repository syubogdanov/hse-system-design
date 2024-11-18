from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    ALREADY_EXISTS = "The order already exists"
    BROKEN_ORDER = "The order of tasks is broken"
    RUNNER_NOT_FOUND = "The task's runner was not found"
    WRONG_TASK = "The wrong task was launched"
