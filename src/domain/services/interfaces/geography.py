from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from pydantic import NonNegativeFloat


class GeographyInterface(Protocol):
    """Интерфейс географии."""

    @abstractmethod
    async def get_zone(self: Self, address_id: UUID) -> UUID:
        """Получить идентификатор области."""

    @abstractmethod
    async def get_load_factor(self: Self, zone_id: UUID) -> "NonNegativeFloat":
        """Получить коэффициент загруженности области."""

    @abstractmethod
    async def get_distance(
        self: Self,
        source_address_id: UUID,
        target_address_id: UUID,
    ) -> "NonNegativeFloat":
        """Получить расстояние между адресами."""
