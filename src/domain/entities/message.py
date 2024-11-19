from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    CONFIGURATION_NOT_FOUND = "The configuration was not found"
    JOB_ALREADY_EXISTS = "The job already exists"
    TASK_RUNNER_NOT_FOUND = "The runner was not found"
    WRONG_TASK_ORDER = "The tasks are executed in the wrong order"
    WRONG_TASK_RUNNER = "The wrong task runner was selected"
