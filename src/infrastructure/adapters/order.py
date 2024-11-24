from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID
from datetime import datetime

from sqlalchemy.sql import select, update, delete

from src.domain.entities.order import Order, OrderParameters
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.order import OrderInterface
from src.infrastructure.models.order import OrderModel
from src.infrastructure.adapters.constants import retry_database

if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class OrderAdapter(OrderInterface):
    """Адаптер заказа."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _order_model: ClassVar = OrderModel

    @retry_database
    async def get(self: Self, order_id: UUID) -> "Order":
        """Получить заказ по идентификатору."""
        query = select(self._order_model).where(self._order_model.id == order_id)

        async with self._session_factory() as session:
            query_result = await session.execute(query)

            if not (model := query_result.scalar()):
                detail = "The order was not found"
                raise NotFoundError(detail)

            return Order.model_validate(model)

    @retry_database
    async def register(self: Self, parameters: "OrderParameters") -> "Order | None":
        """Зарегистрировать заказ."""
        select_query = select(self._order_model).where(self._order_model.id == parameters.id)

        async with self._session_factory() as session:
            select_result = await session.execute(select_query)
            existing_order = select_result.scalar()

            if existing_order is not None:
                return Order.model_validate(existing_order)

            new_order = self._order_model(
                id=parameters.id,
                source_address_id=parameters.source_address_id,
                target_address_id=parameters.target_address_id,
                registered_at=datetime.utcnow()
            )

            session.add(new_order)
            await session.commit()

            return Order.model_validate(new_order)

    @retry_database
    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
        cutoff_time = datetime.utcnow() - retention

        async with self._session_factory() as session:
            delete_query = delete(self._order_model).where(self._order_model.registered_at < cutoff_time)
            await session.execute(delete_query)
            await session.commit()
