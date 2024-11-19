from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.configuration import Configuration
    from src.domain.entities.order import Order
    from src.domain.entities.pricing import Pricing


class PricingInterface(Protocol):
    """Интерфейс ценообразования."""

    @abstractmethod
    async def estimate(self: Self, order: "Order", configuration: "Configuration") -> "Pricing":
        """Проверить, существует ли заказ."""

    @abstractmethod
    async def update_or_create(self: Self, pricing: "Pricing") -> None:
        """Обновить или сохранить сущность."""
