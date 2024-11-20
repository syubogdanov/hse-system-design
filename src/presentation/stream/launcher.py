import asyncio

from typing import Self

from src.container import CONTAINER
from src.presentation.stream.routines import process
from utils.asyncio import waitmap


class StreamLauncher:
    """Лаунчер потока."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить поток."""
        consumer = CONTAINER.kafka_consumer()
        logger = CONTAINER.logger()
        settings = CONTAINER.pipeline_settings()

        logger.info("Starting the stream...")

        asyncio.run(waitmap(process, consumer.consume(), settings.max_concurrent_stages))
