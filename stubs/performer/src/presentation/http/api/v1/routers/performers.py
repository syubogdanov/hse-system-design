from typing import Final
from uuid import UUID

from fastapi import APIRouter

from src.container import CONTAINER
from src.domain.entities.performer import Performer


TAG: Final[str] = "performers"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/nearest")
async def get_nearest(zone_id: UUID) -> list[Performer]:
    """Получить список ближайших к зоне исполнителей."""
    adapter = CONTAINER.performer_adapter()

    return await adapter.get_nearest(zone_id)
