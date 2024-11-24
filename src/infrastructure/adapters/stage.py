from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy import select, update

from src.domain.entities.stage import Stage
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.stage import StageInterface
from src.infrastructure.models.stage import StageModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class StageAdapter(StageInterface):
    """Адаптер этапа."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _stage_model: ClassVar = StageModel

    async def update_or_create(self: Self, stage: "Stage") -> None:
        """Обновить или сохранить этап."""
        stage_as_dict = stage.model_dump()

        update_query = (
            update(self._stage_model)
            .where(self._stage_model.id == stage.id)
            .values(**stage_as_dict)
        )

        async with self._session_factory() as session:
            query_result = await session.execute(update_query)

            if not query_result.rowcount:
                model = self._stage_model(**stage_as_dict)
                session.add(model)

    async def get(self: Self, stage_id: UUID) -> "Stage":
        """Получить этап по идентификатору."""
        query = select(self._stage_model).where(self._stage_model.id == stage_id)

        async with self._session_factory() as session:
            query_result = await session.execute(query)

            if not (model := query_result.scalar()):
                detail = "The stage was not found"
                raise NotFoundError(detail)

            return Stage.model_validate(model)

    async def get_all(self: Self, *, pipeline_id: UUID | None = None) -> list["Stage"]:
        """Получить список всех этапов."""
        query = select(self._stage_model)

        if pipeline_id is not None:
            query = query.where(self._stage_model.pipeline_id == pipeline_id)

        async with self._session_factory() as session:
            query_result = await session.scalars(query)
            models = query_result.all()

            return [Stage.model_validate(model) for model in models]

    async def get_latest(self: Self, pipeline_id: UUID) -> "Stage | None":
        """Получить последний созданный этап."""
        query = (
            select(self._stage_model)
            .where(self._stage_model.pipeline_id == pipeline_id)
            .order_by(self._stage_model.created_at.desc())
            .limit(1)
        )

        async with self._session_factory() as session:
            query_result = await session.execute(query)
            model = query_result.scalar()

            return Stage.model_validate(model) if model is not None else None
