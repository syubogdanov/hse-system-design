from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.message import Message
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import ServiceError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.pipeline import PipelineName
    from src.domain.services.pipelines.base import BasePipeline


@dataclass
class PipelineLauncher:
    """Пайплайн лаунчер."""

    _logger: "Logger"
    _runners: dict["PipelineName", "BasePipeline"]

    async def launch(self: Self, trigger: Trigger) -> None:
        """Отправить триггер на выполнение."""
        runner = self._runners.get(trigger.pipeline)

        if runner is None:
            self._logger.critical(Message.RUNNER_NOT_FOUND, extra={"trigger": trigger})
            raise ServiceError(Message.RUNNER_NOT_FOUND)

        await runner.run(trigger)

        ...
