from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage


@dataclass
class AssignPerformerRunner(StageRunner):
    """Назначить исполнителя на заказ."""

    _logger: "Logger"

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        raise NotImplementedError