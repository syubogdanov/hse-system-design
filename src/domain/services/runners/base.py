from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.stage import Stage


class StageRunner(Protocol):
    """Интерфейс раннера этапов."""

    @abstractmethod
    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
