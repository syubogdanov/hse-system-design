from typing import Final

from fastapi import APIRouter


TAG: Final[str] = "jobs"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])
