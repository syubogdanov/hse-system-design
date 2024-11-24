from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.entities.stage import Stage
from src.domain.entities.status import Status
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import PipelineError, StageError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.result import Result
    from src.domain.entities.stage import StageName
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import StageRunner


@dataclass
class StageLauncher:
    """Лаунчер этапов."""

    _id_factory: Callable[[], UUID]
    _logger: "Logger"
    _pipelines: "PipelineInterface"
    _runners: dict["StageName", "StageRunner"]
    _stages: "StageInterface"
    _triggers: "TriggerInterface"

    async def start(self: Self, trigger: "Trigger") -> None:
        """Начать выполнение пайплайна по заказу."""
        pipeline = await self._pipelines.get(trigger.pipeline_id)

        async with self._pipelines.lock(pipeline.order_id):
            # [!] Сущность выше была получена без блокировки
            pipeline = await self._pipelines.get(pipeline.id)

            if pipeline.status == Status.CANCELED:
                detail = "The pipeline is already canceled"
                raise PipelineError(detail)

            stage = Stage(
                id=self._id_factory(),
                pipeline_id=trigger.pipeline_id,
                name=trigger.stage_name,
            )

            await self._stages.update_or_create(stage)

            runner = self._runners[stage.name]
            stage = await runner.run(stage)

            if stage.status.is_final():
                await self._push_next_or_finish(stage)

    async def resume(self: Self, result: "Result") -> None:
        """Продолжить выполнение пайплайна по заказу."""
        stage = await self._stages.get(result.stage_id)
        pipeline = await self._pipelines.get(stage.pipeline_id)

        async with self._pipelines.lock(pipeline.order_id):
            # [!] Сущность выше была получена без блокировки
            stage = await self._stages.get(stage.id)

            if stage.status.is_final():
                detail = "The stage is already finished"
                raise StageError(detail)

            # Можно не проверять, что пайплайн был отменен, потому что в таком
            # случае асинхронный этап тоже бы был отменен, что мы проверили на
            # пару строк выше.

            stage.finish(result.status, result.message)
            await self._stages.update_or_create(stage)

            await self._push_next_or_finish(stage)

    async def _push_next_or_finish(self: Self, stage: "Stage") -> None:
        """Запустить следующий этап или завершить исполнение."""
        if stage.status != Status.SUCCEEDED:
            pipeline = await self._pipelines.get(stage.pipeline_id)
            pipeline.finish(stage.status, stage.message)
            await self._pipelines.update_or_create(pipeline)

        elif next_stage := stage.name.get_next():
            trigger = Trigger(pipeline_id=stage.pipeline_id, stage_name=next_stage)
            await self._triggers.push(trigger)

        else:
            pipeline = await self._pipelines.get(stage.pipeline_id)
            pipeline.finish(Status.SUCCEEDED)
            await self._pipelines.update_or_create(pipeline)
