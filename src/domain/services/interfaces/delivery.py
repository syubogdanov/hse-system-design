from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.delivery import Delivery


class DeliveryInterface(Protocol):
    """Интерфейс доставки."""

    @abstractmethod
    async def get(self: Self, pipeline_id: UUID) -> "Delivery | None":
        """Получить доставку по идентификатору пайплайна."""

    @abstractmethod
    async def update_or_create(self: Self, delivery: "Delivery") -> None:
        """Обновить или сохранить доставку."""
