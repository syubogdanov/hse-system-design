from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.trigger import Trigger


class BasePipeline(Protocol):
    """Интерфейс пайплайн-раннера."""

    @abstractmethod
    async def run(self: Self, trigger: "Trigger") -> "Trigger":
        """Запустить пайплайн."""
