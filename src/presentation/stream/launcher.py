import asyncio

from typing import Self

from src.container import CONTAINER
from src.presentation.stream.routines import process
from utils.itertools import aiomap


class StreamLauncher:
    """Лаунчер потока."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить поток."""
        consumer = CONTAINER.kafka_consumer()
        settings = CONTAINER.stream_settings()

        coroutine = aiomap(process, consumer.consume(), settings.max_concurrent_tasks)

        asyncio.run(coroutine)
