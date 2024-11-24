from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy.sql import select, update

from src.domain.entities.pipeline import Pipeline
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.pipeline import PipelineInterface
from src.infrastructure.adapters.constants import retry_database
from src.infrastructure.models.pipeline import PipelineModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _pipeline_model: ClassVar = PipelineModel

    @retry_database
    async def get(self: Self, pipeline_id: UUID) -> "Pipeline":
        """Получить пайплайн по идентификатору."""
        query = select(self._pipeline_model).where(self._pipeline_model.id == pipeline_id)

        async with self._session_factory() as session:
            query_result = await session.execute(query)

            if not (model := query_result.scalar()):
                detail = "The pipeline was not found"
                raise NotFoundError(detail)

            return Pipeline.model_validate(model)

    @retry_database
    async def get_all(self: Self, *, order_id: UUID | None = None) -> list["Pipeline"]:
        """Получить список всех пайплайнов."""
        query = select(self._pipeline_model)

        if order_id is not None:
            query = query.where(self._pipeline_model.order_id == order_id)

        async with self._session_factory() as session:
            query_result = await session.scalars(query)
            models = query_result.all()

            return [Pipeline.model_validate(model) for model in models]

    @retry_database
    async def update_or_create(self: Self, pipeline: "Pipeline") -> None:
        """Обновить или сохранить пайплайн."""
        pipeline_as_dict = pipeline.model_dump()

        update_query = (
            update(self._pipeline_model)
            .where(self._pipeline_model.id == pipeline.id)
            .values(**pipeline_as_dict)
        )

        async with self._session_factory() as session:
            query_result = await session.execute(update_query)

            if not query_result.rowcount:
                model = self._pipeline_model(**pipeline_as_dict)
                session.add(model)

    @retry_database
    async def get_latest(self: Self, order_id: UUID) -> "Pipeline | None":
        """Получить последний созданный пайплайн."""
        query = (
            select(self._pipeline_model)
            .where(self._pipeline_model.order_id == order_id)
            .order_by(self._pipeline_model.created_at.desc())
            .limit(1)
        )

        async with self._session_factory() as session:
            query_result = await session.execute(query)
            model = query_result.scalar()

            return Pipeline.model_validate(model) if model is not None else None

    def lock(self: Self, order_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение пайплайнов по заказу."""
        raise NotImplementedError
