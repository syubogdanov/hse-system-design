from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.pipeline import Pipeline
    from src.domain.entities.stage import Stage


class PipelineInterface(Protocol):
    """Интерфейс пайплайна."""

    @abstractmethod
    async def get(self: Self, pipeline_id: UUID) -> "Pipeline":
        """Получить пайплайн по идентфикатору."""

    @abstractmethod
    async def get_all(self: Self) -> list["Pipeline"]:
        """Получить список всех пайплайнов."""

    @abstractmethod
    async def get_stages(self: Self, pipeline_id: UUID) -> list["Stage"]:
        """Получить этапы пайплайна."""

    @abstractmethod
    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""
