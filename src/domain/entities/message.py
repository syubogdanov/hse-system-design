from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    BROKEN_TASK_ORDER = "The order of tasks is broken"
    CONFIGURATION_NOT_FOUND = ""
    ORDER_ALREADY_EXISTS = "The order already exists"
    RUNNER_NOT_FOUND = "The runner was not found"
    WRONG_RUNNER = "The wrong runner was selected"
