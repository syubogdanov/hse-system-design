from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.geography import GeographyInterface


if TYPE_CHECKING:
    from pydantic import NonNegativeFloat


class GeographyAdapter(GeographyInterface):
    """Интерфейс географии."""

    async def get_zone(self: Self, address_id: UUID) -> UUID:
        """Получить идентификатор области."""
        raise NotImplementedError

    async def get_load_factor(self: Self, zone_id: UUID) -> "NonNegativeFloat":
        """Получить коэффициент загруженности области."""
        raise NotImplementedError

    async def get_distance(
        self: Self,
        source_address_id: UUID,
        target_address_id: UUID,
    ) -> "NonNegativeFloat":
        """Получить расстояние между адресами."""
        raise NotImplementedError
