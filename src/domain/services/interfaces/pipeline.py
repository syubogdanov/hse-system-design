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
    async def get_all(self: Self, *, order_id: UUID | None = None) -> list["Pipeline"]:
        """Получить список всех пайплайнов."""

    @abstractmethod
    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""

    @abstractmethod
    async def get_latest(self: Self, order_id: UUID) -> "Pipeline | None":
        """Получить последний созданный пайплайн."""

    @abstractmethod
    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение пайплайнов по заказу."""

    @abstractmethod
    async def exists(self: Self, pipeline_id: UUID) -> bool:
        """Проверить, что пайплайн существует."""
