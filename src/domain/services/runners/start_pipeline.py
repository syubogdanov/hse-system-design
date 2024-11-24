import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.delivery import Delivery
from src.domain.entities.status import Status
from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage
    from src.domain.services.interfaces.delivery import DeliveryInterface
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface


@dataclass
class StartPipelineRunner(StageRunner):
    """Инициализация пайплайна."""

    _deliveries: "DeliveryInterface"
    _logger: "Logger"
    _pipelines: "PipelineInterface"
    _stages: "StageInterface"

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        pipeline = await self._pipelines.get(stage.pipeline_id)

        pipeline.start()
        stage.start()

        delivery = Delivery(pipeline_id=pipeline.id)

        stage.finish(Status.SUCCEEDED)

        await asyncio.gather(
            self._pipelines.update_or_create(pipeline),
            self._stages.update_or_create(stage),
            self._deliveries.update_or_create(delivery),
        )

        return stage
