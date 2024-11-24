from typing import Final
from uuid import UUID

from fastapi import APIRouter
from pydantic import NonNegativeFloat

from src.container import CONTAINER


TAG: Final[str] = "math"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/distance")
async def get_distance(source_address_id: UUID, target_address_id: UUID) -> NonNegativeFloat:
    """Получить расстояние между двумя адресами."""
    adapter = CONTAINER.math_adapter()

    return await adapter.get_distance(source_address_id, target_address_id)


@router.get("/load-factor")
async def get_load_factor(zone_id: UUID) -> NonNegativeFloat:
    """Получить коэффициент нагруженности области."""
    adapter = CONTAINER.math_adapter()

    return await adapter.get_load_factor(zone_id)
