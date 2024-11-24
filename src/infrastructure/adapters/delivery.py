from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.delivery import DeliveryInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.delivery import Delivery


@dataclass
class DeliveryAdapter(DeliveryInterface):
    """Адаптер доставки."""

    _logger: "Logger"

    async def get(self: Self, pipeline_id: UUID) -> "Delivery":
        """Получить доставку по идентификатору пайплайна."""
        raise NotImplementedError

    async def update_or_create(self: Self, delivery: "Delivery") -> None:
        """Обновить или сохранить доставку."""
        raise NotImplementedError
