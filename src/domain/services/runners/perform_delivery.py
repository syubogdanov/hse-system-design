from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage
    from src.domain.services.interfaces.stage import StageInterface


@dataclass
class PerformDeliveryRunner(StageRunner):
    """Начать выполнение доставки."""

    _logger: "Logger"
    _stages: "StageInterface"

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        stage.start()
        await self._stages.update_or_create(stage)

        return stage
