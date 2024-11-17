from logging import INFO, basicConfig, getLogger
from typing import TYPE_CHECKING, Final


if TYPE_CHECKING:
    from logging import Logger


FORMAT: Final[str] = "%(levelname)s [%(asctime)s] %(message)s"


def get_logger(*, name: str = __name__, level: int = INFO) -> "Logger":
    """Фабрика логгеров."""
    basicConfig(format=FORMAT)

    logger = getLogger(name)
    logger.setLevel(level)

    return logger
