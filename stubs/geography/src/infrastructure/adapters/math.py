import asyncio

from random import uniform
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.math import MathInterface


if TYPE_CHECKING:
    from pydantic import NonNegativeFloat


class MathAdapter(MathInterface):
    """Адаптер вычислений."""

    _min_load_factor: ClassVar[float] = 0.5
    _max_load_factor: ClassVar[float] = 2.5

    _min_distance: ClassVar[float] = 1.0
    _max_distance: ClassVar[float] = 75000.0

    _precision: ClassVar[int] = 2
    _probability: ClassVar[float] = 0.05

    async def get_load_factor(self: Self, zone_id: UUID) -> "NonNegativeFloat":
        """Получить коэффициент загруженности области."""
        if not await self._zone_exists(zone_id):
            detail = "The zone was not found"
            raise NotFoundError(detail)

        load_factor = uniform(self._min_load_factor, self._max_load_factor)
        return round(load_factor, self._precision)

    async def get_distance(
        self: Self,
        source_address_id: UUID,
        target_address_id: UUID,
    ) -> "NonNegativeFloat":
        """Получить расстояние между адресами."""
        source_exists, target_exists = await asyncio.gather(
            self._address_exists(source_address_id),
            self._address_exists(target_address_id),
        )

        if not source_exists and not target_exists:
            detail = "One of the addresses was not found"
            raise NotFoundError(detail)

        distance = uniform(self._min_distance, self._max_distance)
        return round(distance, self._precision)

    async def _address_exists(self: Self, _address_id: UUID) -> bool:
        """Проверить, что адрес существует."""
        return uniform(0.0, 1.0) >= self._probability

    async def _zone_exists(self: Self, _address_id: UUID) -> bool:
        """Проверить, что область существует."""
        return uniform(0.0, 1.0) >= self._probability
