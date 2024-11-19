from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from src.domain.entities.configuration import Configuration
    from src.domain.entities.job import Job
    from src.domain.entities.pricing import Pricing


class PricingInterface(Protocol):
    """Интерфейс ценообразования."""

    @abstractmethod
    async def estimate(self: Self, job: "Job", configuration: "Configuration") -> "Pricing":
        """Оценить стоимость выполнения работы."""

    @abstractmethod
    async def update_or_create(self: Self, pricing: "Pricing") -> None:
        """Обновить или сохранить правило ценообразование."""
