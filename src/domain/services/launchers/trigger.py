from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.message import Message
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import DeveloperError, StageError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import StageName
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import StageRunner


@dataclass
class TriggerLauncher:
    """Лаунчер триггеров."""

    _logger: "Logger"
    _pipelines: "PipelineInterface"
    _runners: dict["StageName", "StageRunner"]
    _stages: "StageInterface"
    _triggers: "TriggerInterface"

    async def launch(self: Self, trigger: Trigger) -> None:
        """Запустить триггер-событие."""
        if not (runner := self._runners.get(trigger.stage_name)):
            raise DeveloperError(Message.STAGE_RUNNER_NOT_FOUND)

        async with self._stages.lock(trigger.pipeline_id):
            if await self._pipelines.is_canceled(trigger.pipeline_id):
                return

            if not await runner.is_runnable(trigger):
                raise StageError(Message.STAGE_RUNNER_NOT_RUNNABLE)

            await runner.run(trigger)

        if (next_stage := trigger.stage_name.get_next()) and next_stage.is_schedulable():
            next_trigger = trigger.model_copy(update={"stage_name": next_stage})
            await self._triggers.push(next_trigger)
