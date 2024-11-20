from typing import Final

from fastapi import APIRouter


TAG: Final[str] = "pipelines"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])
