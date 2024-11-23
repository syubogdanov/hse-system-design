from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.pipeline import PipelineInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.pipeline import Pipeline


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"

    async def get(self: Self, pipeline_id: UUID) -> "Pipeline":
        """Получить пайплайн по идентификатору."""
        raise NotImplementedError

    async def get_all(self: Self, *, order_id: UUID | None = None) -> list["Pipeline"]:
        """Получить список всех пайплайнов."""
        raise NotImplementedError

    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""
        raise NotImplementedError

    async def get_latest(self: Self, order_id: UUID) -> "Pipeline | None":
        """Получить последний запущенный пайплайн."""
        raise NotImplementedError

    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение пайплайнов по заказу."""
        raise NotImplementedError
