from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.entities.pipeline import Pipeline
from src.domain.entities.stage import StageName
from src.domain.entities.status import Status
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import NotFoundError, PipelineError, StageError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface
    from src.domain.services.interfaces.trigger import TriggerInterface


@dataclass
class PipelineLauncher:
    """Лаунчер пайплайнов."""

    _id_factory: Callable[[], UUID]
    _logger: "Logger"
    _pipelines: "PipelineInterface"
    _stages: "StageInterface"
    _triggers: "TriggerInterface"

    async def start(self: Self, order_id: UUID) -> UUID:
        """Начать выполнение пайплайна по заказу."""
        async with self._pipelines.lock(order_id):
            latest = await self._pipelines.get_latest(order_id)

            if latest and not latest.status.is_final():
                detail = "There is a running pipeline"
                raise PipelineError(detail, latest)

            if latest and not latest.is_restartable():
                detail = "The pipeline cannot be restarted"
                raise PipelineError(detail, latest)

            pipeline = Pipeline(id=self._id_factory(), order_id=order_id)
            await self._pipelines.update_or_create(pipeline)

            trigger = Trigger(pipeline_id=pipeline.id, stage_name=StageName.first())
            await self._triggers.push(trigger)

            return pipeline.id

    async def cancel(self: Self, order_id: UUID) -> None:
        """Отменить выполнение пайплайна по заказу."""
        async with self._pipelines.lock(order_id):
            pipeline = await self._pipelines.get_latest(order_id)

            if not pipeline:
                detail = "No pipelines have been launched yet"
                raise NotFoundError(detail, order_id)

            if pipeline.status.is_final():
                detail = "The pipeline has already been finished"
                raise PipelineError(detail, pipeline)

            stage = await self._stages.get_latest(pipeline.id)

            if stage and not stage.name.is_cancelable():
                detail = "The current stage is not cancelable"
                raise StageError(detail, stage)

            if stage and not stage.status.is_final():
                stage.finish(Status.CANCELED)
                await self._stages.update_or_create(stage)

            pipeline.finish(Status.CANCELED)
            await self._pipelines.update_or_create(pipeline)
