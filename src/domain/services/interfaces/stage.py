from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.stage import Stage


class StageInterface(Protocol):
    """Интерфейс этапа."""

    @abstractmethod
    async def update_or_create(self: Self, stage: "Stage") -> None:
        """Обновить или сохранить этап."""

    @abstractmethod
    async def get(self: Self, stage_id: UUID) -> "Stage":
        """Получить этап по идентификатору."""

    @abstractmethod
    async def get_all(self: Self, *, pipeline_id: UUID | None = None) -> list["Stage"]:
        """Получить список всех этапов."""

    @abstractmethod
    async def get_latest(self: Self, pipeline_id: UUID) -> "Stage | None":
        """Получить последний запущенный этап."""
