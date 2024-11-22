from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.pipeline import Pipeline


class PipelineInterface(Protocol):
    """Интерфейс пайплайна."""

    @abstractmethod
    async def get(self: Self, pipeline_id: UUID) -> "Pipeline":
        """Получить пайплайн по идентификатору."""

    @abstractmethod
    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""

    @abstractmethod
    async def get_latest(self: Self, order_id: UUID) -> "Pipeline | None":
        """Получить последний запущенный пайплайн."""

    @abstractmethod
    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение пайплайнов по заказу."""
