import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import NotFoundError, ParametersError, TaskError
from src.domain.services.runners.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.domain.services.interfaces.configuration import ConfigurationInterface
    from src.domain.services.interfaces.job import JobInterface
    from src.domain.services.interfaces.pricing import PricingInterface


@dataclass
class EstimationRunner(TaskRunner):
    """Задача оценки стоимости заказа."""

    _configuration: "ConfigurationInterface"
    _jobs: "JobInterface"
    _logger: "Logger"
    _pricing: "PricingInterface"

    _task: ClassVar[TaskName] = TaskName.ESTIMATE

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_TASK_RUNNER)

        async with self._jobs.lock(trigger.job_id):
            job = await self._jobs.get(trigger.job_id)

            if job.task not in self._task.get_previous():
                raise TaskError(Message.WRONG_TASK_ORDER)

            if (configuration := await self._configuration.get()) is None:
                raise NotFoundError(Message.CONFIGURATION_NOT_FOUND)

            pricing = await self._pricing.estimate(job, configuration)
            job.complete_task(self._task)

            await asyncio.gather(
                self._pricing.update_or_create(pricing),
                self._jobs.update_or_create(job),
            )
