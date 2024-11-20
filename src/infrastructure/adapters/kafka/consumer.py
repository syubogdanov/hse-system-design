from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from aiokafka.consumer import AIOKafkaConsumer


if TYPE_CHECKING:
    from logging import Logger

    from src.infrastructure.settings.kafka import KafkaSettings


@dataclass
class KafkaConsumerAdapter:
    """Адаптер консьюмера `Kafka`."""

    _logger: "Logger"
    _settings: "KafkaSettings"

    def __post_init__(self: Self) -> None:
        """Дополнительная инициализация объекта."""
        self._consumer = AIOKafkaConsumer(
            self._settings.topic_name,
            bootstrap_servers=self._settings.bootstrap_servers,
            client_id=self._settings.client_id,
            group_id=self._settings.group_id,
        )

    async def consume(self: Self) -> AsyncIterator[bytes]:
        """Бесконечно вычитывать сообщения из топика."""
        async with self._consumer as context:
            async for event in context:
                yield event.value
