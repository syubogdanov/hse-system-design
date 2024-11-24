from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.container import CONTAINER
from src.domain.entities.zone import Zone


TAG: Final[str] = "address"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{id}/zone")
async def get_zone(address_id: Annotated[UUID, Path(alias="id")]) -> Zone:
    """Получить область, в которой находится адрес."""
    adapter = CONTAINER.address_adapter()

    return await adapter.get_zone(address_id)
