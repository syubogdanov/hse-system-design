from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger


@dataclass
class ReleaseRunner(StageRunner):
    """Освободить исполнителя от заказа."""

    _logger: "Logger"

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить этап по триггеру."""
        raise NotImplementedError
