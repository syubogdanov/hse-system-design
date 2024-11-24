from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from uuid import UUID

from src.domain.services.interfaces.geography import GeographyInterface
from src.infrastructure.adapters.constants import retry_external_api


if TYPE_CHECKING:
    from logging import Logger

    from pydantic import NonNegativeFloat

    from src.domain.entities.zone import Zone


@dataclass
class GeographyAdapter(GeographyInterface):
    """Интерфейс географии."""

    _logger: "Logger"

    @retry_external_api
    async def get_zone(self: Self, address_id: UUID) -> "Zone":
        """Получить идентификатор области."""
        raise NotImplementedError

    @retry_external_api
    async def get_load_factor(self: Self, zone_id: UUID) -> "NonNegativeFloat":
        """Получить коэффициент загруженности области."""
        raise NotImplementedError

    @retry_external_api
    async def get_distance(
        self: Self,
        source_address_id: UUID,
        target_address_id: UUID,
    ) -> "NonNegativeFloat":
        """Получить расстояние между адресами."""
        raise NotImplementedError
