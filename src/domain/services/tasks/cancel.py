from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import ParametersError
from src.domain.services.tasks.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger


@dataclass
class CancellationTask(TaskRunner):
    """Задача отмены назначения."""

    _logger: "Logger"

    _task: ClassVar[TaskName] = TaskName.CANCEL

    async def run(self: Self, trigger: "Trigger") -> "Trigger":
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_TASK)

        ...
