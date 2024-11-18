from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.message import Message
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import ServiceError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.task import TaskName
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.tasks.base import TaskRunner


@dataclass
class TaskLauncher:
    """Лаунчер задач."""

    _logger: "Logger"
    _next_tasks: dict["TaskName", "TaskName"]
    _runners: dict["TaskName", "TaskRunner"]
    _trigger: "TriggerInterface"

    async def launch(self: Self, trigger: Trigger) -> None:
        """Запустить выполнение триггер-события."""
        runner = self._runners.get(trigger.task)

        if runner is None:
            self._logger.critical(Message.RUNNER_NOT_FOUND, extra={"trigger": trigger})
            raise ServiceError(Message.RUNNER_NOT_FOUND)

        trigger = await runner.run(trigger)

        next_task = self._next_tasks.get(trigger.task)

        if next_task is not None:
            next_trigger = trigger.model_copy(update={"task": next_task})
            await self._trigger.push(next_trigger)
