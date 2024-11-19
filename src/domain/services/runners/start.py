from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.job import Job
from src.domain.entities.message import Message
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import ParametersError, TaskError
from src.domain.services.runners.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.domain.services.interfaces.job import JobInterface


@dataclass
class StartingRunner(TaskRunner):
    """Задача запуска назначения."""

    _logger: "Logger"
    _order: "JobInterface"

    _task: ClassVar[TaskName] = TaskName.START

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_TASK_RUNNER)

        async with self._order.lock(trigger.job_id):
            if await self._order.exists(trigger.job_id):
                raise TaskError(Message.JOB_ALREADY_EXISTS)

            order = Job(id=trigger.job_id, task=self._task)
            await self._order.update_or_create(order)
