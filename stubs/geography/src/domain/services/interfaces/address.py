from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.zone import Zone


class AddressInterface(Protocol):
    """Интерфейс адреса."""

    @abstractmethod
    async def get_zone(self: Self, address_id: UUID) -> "Zone":
        """Получить область, соответствующую адресу."""
