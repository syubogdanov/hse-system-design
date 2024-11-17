from enum import StrEnum


class Message(StrEnum):
    """Сообщение."""

    RUNNER_NOT_FOUND = "The pipeline's runner was not found"
    WRONG_PIPELINE = "The wrong pipeline was launched"
