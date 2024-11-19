from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.message import Message
from src.domain.entities.trigger import Trigger
from src.domain.services.exceptions import ServiceError


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.task import TaskName
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import TaskRunner


@dataclass
class TriggerLauncher:
    """Лаунчер триггеров."""

    _logger: "Logger"
    _runners: dict["TaskName", "TaskRunner"]
    _trigger: "TriggerInterface"

    async def launch(self: Self, trigger: Trigger) -> None:
        """Запустить выполнение триггер-события."""
        if (runner := self._runners.get(trigger.task)) is None:
            raise ServiceError(Message.TASK_RUNNER_NOT_FOUND)

        await runner.run(trigger)

        if (next_task := trigger.task.get_next()) is not None:
            next_trigger = trigger.model_copy(update={"task": next_task})
            await self._trigger.push(next_trigger)
