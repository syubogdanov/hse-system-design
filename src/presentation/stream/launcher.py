import asyncio

from typing import Self

from src.container import CONTAINER
from src.presentation.stream.routines import on_result, on_trigger
from utils.asyncio import waitmap


class StreamLauncher:
    """Лаунчер потока."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить поток."""
        logger = CONTAINER.logger()

        logger.info("Starting the stream...")

        asyncio.run(cls._run_stream())

    @classmethod
    async def _run_stream(cls: type[Self]) -> None:
        """Вычитывать и обрабатывать сообщения."""
        logger = CONTAINER.logger()
        consumer = CONTAINER.kafka_consumer_adapter()
        topic_name_settings = CONTAINER.topic_name_settings()
        pipeline_settings = CONTAINER.pipeline_settings()

        await asyncio.gather(
            waitmap(
                on_result,
                consumer.consume(topic_name_settings.results),
                max_concurrent_tasks=pipeline_settings.max_concurrent_results,
                logger=logger,
            ),
            waitmap(
                on_trigger,
                consumer.consume(topic_name_settings.triggers),
                max_concurrent_tasks=pipeline_settings.max_concurrent_triggers,
                logger=logger,
            ),
        )
