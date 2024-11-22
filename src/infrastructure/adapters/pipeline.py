from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.pipeline import PipelineInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.pipeline import Pipeline
    from src.domain.entities.stage import Stage


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"

    async def get(self: Self, pipeline_id: UUID) -> "Pipeline":
        """Получить пайплайн по идентфикатору."""
        raise NotImplementedError

    async def get_all(self: Self) -> list["Pipeline"]:
        """Получить список всех пайплайнов."""
        raise NotImplementedError

    async def get_stages(self: Self, pipeline_id: UUID) -> list["Stage"]:
        """Получить этапы пайплайна."""
        raise NotImplementedError

    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""
        raise NotImplementedError
