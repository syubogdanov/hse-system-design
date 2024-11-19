from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import ParametersError, TaskError
from src.domain.services.runners.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.domain.services.interfaces.job import JobInterface


@dataclass
class AssignmentRunner(TaskRunner):
    """Задача назначения исполнителя."""

    _jobs: "JobInterface"
    _logger: "Logger"

    _task: ClassVar[TaskName] = TaskName.ASSIGN

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_TASK_RUNNER)

        async with self._jobs.lock(trigger.job_id):
            job = await self._jobs.get(trigger.job_id)

            if job.task not in self._task.get_previous():
                raise TaskError(Message.WRONG_TASK_ORDER)

            ...
