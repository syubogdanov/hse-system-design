from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy.sql import exists, select, update

from src.domain.entities.delivery import Delivery
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.delivery import DeliveryInterface
from src.infrastructure.adapters.constants import retry_database
from src.infrastructure.models.delivery import DeliveryModel
from src.infrastructure.models.pipeline import PipelineModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class DeliveryAdapter(DeliveryInterface):
    """Адаптер доставки."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _delivery_model: ClassVar = DeliveryModel
    _pipeline_model: ClassVar = PipelineModel

    @retry_database
    async def get(self: Self, pipeline_id: UUID) -> "Delivery":
        """Получить доставку по идентификатору пайплайна."""
        exists_query = select(exists().where(self._pipeline_model.id == pipeline_id))

        select_query = (
            select(self._delivery_model)
            .where(self._delivery_model.pipeline_id == pipeline_id)
        )

        async with self._session_factory() as session:
            exists_query_result = await session.execute(exists_query)
            pipeline_exists = bool(exists_query_result.scalar())

            if not pipeline_exists:
                detail = "The pipeline was not found"
                raise NotFoundError(detail)

            query_result = await session.execute(select_query)

            if not (model := query_result.scalar()):
                detail = "The delivery was not found"
                raise NotFoundError(detail)

            return Delivery.model_validate(model)

    @retry_database
    async def update_or_create(self: Self, delivery: "Delivery") -> None:
        """Обновить или сохранить доставку."""
        delivery_as_dict = delivery.model_dump()

        update_query = (
            update(self._delivery_model)
            .where(self._delivery_model.pipeline_id == delivery.pipeline_id)
            .values(**delivery_as_dict)
        )

        async with self._session_factory() as session:
            query_result = await session.execute(update_query)

            if not query_result.rowcount:
                model = self._delivery_model(**delivery_as_dict)
                session.add(model)
