from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, Path

from src.container import CONTAINER
from src.domain.entities.performer import Performer


TAG: Final[str] = "performers"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_all() -> list[Performer]:
    """Получить список всех исполнителей."""
    adapter = CONTAINER.performer_adapter()

    return await adapter.get_all()


@router.get("/{id}")
async def get(id_: Annotated[UUID, Path(alias="id")]) -> Performer:
    """Получить исполнителя по идентификатору."""
    adapter = CONTAINER.performer_adapter()

    return await adapter.get(id_)
