from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy.sql import exists, select

from src.domain.services.interfaces.performer import PerformerInterface
from src.infrastructure.adapters.constants import retry_database
from src.infrastructure.models.delivery import DeliveryModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class PerformerAdapter(PerformerInterface):
    """Адаптер исполнителя."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _delivery_model: ClassVar = DeliveryModel

    @retry_database
    async def is_busy(self: Self, performer_id: UUID) -> bool:
        """Получить пайплайн по идентификатору."""
        subquery = exists().where(
            self._delivery_model == performer_id,
            self._delivery_model.released_at.is_not(None),
        )

        async with self._session_factory() as session:
            query_result = await session.execute(select(subquery))
            return bool(query_result.scalar())

    def lock(self: Self, performer_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать назначение исполнителя на заказы."""
        raise NotImplementedError
