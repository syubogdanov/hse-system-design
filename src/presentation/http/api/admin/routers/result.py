from http import HTTPStatus
from typing import Final

from fastapi import APIRouter

from src.container import CONTAINER
from src.domain.entities.result import Result


TAG: Final[str] = "results"
PREFIX: Final[str] = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("", status_code=HTTPStatus.ACCEPTED)
async def send(result: Result) -> None:
    """Отправить событие-результат."""
    producer = CONTAINER.kafka_producer_adapter()
    topics = CONTAINER.topic_name_settings()

    return await producer.produce(topics.results, result)
