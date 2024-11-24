from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy.sql import exists, select, update

from src.domain.entities.pipeline import Pipeline
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.pipeline import PipelineInterface
from src.infrastructure.adapters.constants import retry_database
from src.infrastructure.models.order import OrderModel
from src.infrastructure.models.pipeline import PipelineModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class PipelineAdapter(PipelineInterface):
    """Адаптер пайплайна."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _order_model: ClassVar = OrderModel
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
        exists_query = select(exists().where(self._order_model.id == order_id))

        select_query = (
            select(self._pipeline_model)
            .where(self._pipeline_model.order_id == order_id)
            .order_by(self._pipeline_model.created_at.desc())
            .limit(1)
        )

        async with self._session_factory() as session:
            exists_query_result = await session.execute(exists_query)
            order_exists = bool(exists_query_result.scalar())

            if not order_exists:
                detail = "The order was not found"
                raise NotFoundError(detail)

            select_query_result = await session.execute(select_query)
            model = select_query_result.scalar()

            return Pipeline.model_validate(model) if model is not None else None

    @retry_database
    async def exists(self: Self, pipeline_id: UUID) -> bool:
        """Проверить, что пайплайн существует."""
        query = select(exists().where(self._pipeline_model.id == pipeline_id))

        async with self._session_factory() as session:
            query_result = await session.execute(query)
            return bool(query_result.scalar())

    @asynccontextmanager
    async def lock(self: Self, order_id: UUID) -> AsyncGenerator[None, None]:
        """Заблокировать выполнение пайплайнов по заказу."""
        yield
