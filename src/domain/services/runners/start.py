from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.order import Order
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import ParametersError, TaskError
from src.domain.services.runners.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.domain.services.interfaces.order import OrderInterface


@dataclass
class StartingRunner(TaskRunner):
    """Задача запуска назначения."""

    _logger: "Logger"
    _order: "OrderInterface"

    _task: ClassVar[TaskName] = TaskName.START

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_RUNNER)

        async with self._order.lock(trigger.order_id):
            if await self._order.exists(trigger.order_id):
                raise TaskError(Message.ORDER_ALREADY_EXISTS)

            order = Order(id=trigger.order_id, last_task=self._task)
            await self._order.update_or_create(order)
