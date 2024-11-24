from dataclasses import dataclass
from random import uniform
from typing import ClassVar, Self
from uuid import UUID, uuid4

from src.domain.entities.zone import Zone
from src.domain.services.exceptions import NotFoundError
from src.domain.services.interfaces.address import AddressInterface


@dataclass
class AddressAdapter(AddressInterface):
    """Адаптер адреса."""

    _probability: ClassVar[float] = 0.05

    async def get_zone(self: Self, address_id: UUID) -> "Zone":
        """Получить область, соответствующую адресу."""
        if not await self._exists(address_id):
            detail = "The address was not found"
            raise NotFoundError(detail)

        return Zone(id=uuid4())

    async def _exists(self: Self, _address_id: UUID) -> bool:
        """Проверить, что адрес существует."""
        return uniform(0.0, 1.0) >= self._probability
