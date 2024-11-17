from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.message import Message
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import ServiceError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.pipeline import PipelineName
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.pipelines.base import BasePipeline


@dataclass
class PipelineLauncher:
    """Лаунчер триггер-событий."""

    _logger: "Logger"
    _next_pipelines: dict["PipelineName", "PipelineName"]
    _runners: dict["PipelineName", "BasePipeline"]
    _triggers: "TriggerInterface"

    async def launch(self: Self, trigger: Trigger) -> None:
        """Запустить выполнение триггер-события."""
        runner = self._runners.get(trigger.pipeline)

        if runner is None:
            self._logger.critical(Message.RUNNER_NOT_FOUND, extra={"trigger": trigger})
            raise ServiceError(Message.RUNNER_NOT_FOUND)

        trigger = await runner.run(trigger)

        next_pipeline = self._next_pipelines.get(trigger.pipeline)

        if next_pipeline is not None:
            next_trigger = trigger.model_copy(update={"pipeline": next_pipeline})
            await self._triggers.push(next_trigger)
