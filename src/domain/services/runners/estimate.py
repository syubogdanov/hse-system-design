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
    from src.domain.services.interfaces.order import OrderInterface
    from src.domain.services.interfaces.pricing import PricingInterface


@dataclass
class EstimationRunner(TaskRunner):
    """Задача оценки стоимости заказа."""

    _configuration: "ConfigurationInterface"
    _logger: "Logger"
    _order: "OrderInterface"
    _pricing: "PricingInterface"

    _task: ClassVar[TaskName] = TaskName.ESTIMATE

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_RUNNER)

        async with self._order.lock(trigger.order_id):
            order = await self._order.get(trigger.order_id)

            if order.last_task not in self._task.get_previous():
                raise TaskError(Message.BROKEN_TASK_ORDER)

            if (configuration := await self._configuration.get()) is None:
                raise NotFoundError(Message.CONFIGURATION_NOT_FOUND)

            pricing = await self._pricing.estimate(order, configuration)
            order.complete(self._task)

            await asyncio.gather(
                self._order.update_or_create(order),
                self._pricing.update_or_create(pricing),
            )
