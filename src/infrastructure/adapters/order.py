from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from sqlalchemy.sql import delete, select

from src.domain.entities.order import Order, OrderParameters
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.order import OrderInterface
from src.infrastructure.adapters.constants import retry_database
from src.infrastructure.models.order import OrderModel
from utils.datetime import utcnow


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
        """Зарегистрировать заказ, если такого еще не было."""
        query = select(self._order_model).where(self._order_model.id == parameters.id)

        async with self._session_factory() as session:
            query_result = await session.execute(query)

            if (model := query_result.scalar()):
                return None

            order = Order.model_validate(parameters)
            model = self._order_model(**order.model_dump())

            session.add(model)

        return order

    @retry_database
    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
        query = (
            delete(self._order_model)
            .where(self._order_model.registered_at < utcnow() - retention)
        )

        async with self._session_factory() as session:
            await session.execute(query)
