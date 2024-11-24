from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.delivery import DeliveryInterface
from src.infrastructure.adapters.constants import retry_database


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.delivery import Delivery


@dataclass
class DeliveryAdapter(DeliveryInterface):
    """Адаптер доставки."""

    _logger: "Logger"

    @retry_database
    async def get(self: Self, pipeline_id: UUID) -> "Delivery":
        """Получить доставку по идентификатору пайплайна."""
        raise NotImplementedError

    @retry_database
    async def update_or_create(self: Self, delivery: "Delivery") -> None:
        """Обновить или сохранить доставку."""
        raise NotImplementedError
