from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.trigger import Trigger


class StageRunner(Protocol):
    """Интерфейс раннера этапов."""

    @abstractmethod
    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить этап по триггеру."""

    @abstractmethod
    async def is_runnable(self: Self, trigger: "Trigger") -> bool:
        """Проверить, разрешено ли запустить этап по триггеру."""
