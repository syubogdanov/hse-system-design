from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.trigger import Trigger


class TaskRunner(Protocol):
    """Интерфейс раннера задач."""

    @abstractmethod
    async def run(self: Self, trigger: "Trigger") -> "Trigger":
        """Запустить задачу по триггеру."""
