from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.task import TaskName
from src.domain.services.exceptions import ParametersError
from src.domain.services.runners.base import TaskRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.domain.services.interfaces.order import OrderInterface


@dataclass
class AssignmentRunner(TaskRunner):
    """Задача назначения исполнителя."""

    _logger: "Logger"
    _order: "OrderInterface"

    _task: ClassVar[TaskName] = TaskName.ASSIGN

    async def run(self: Self, trigger: "Trigger") -> "Trigger":
        """Запустить задачу по триггеру."""
        if trigger.task != self._task:
            raise ParametersError(Message.WRONG_TASK)

        async with self._order.lock(trigger.order_id):
            ...
