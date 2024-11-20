from logging import basicConfig, getLogger
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from logging import Logger


def get_logger(format_: str, level: int) -> "Logger":
    """Получить логгер."""
    basicConfig(format=format_)

    logger = getLogger()
    logger.setLevel(level)

    return logger
