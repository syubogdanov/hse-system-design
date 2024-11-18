from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from aiokafka.producer import AIOKafkaProducer


if TYPE_CHECKING:
    from logging import Logger

    from src.infrastructure.settings.kafka import KafkaSettings


@dataclass
class KafkaProducerAdapter:
    """Адаптер `Kafka`-продюсера."""

    _logger: "Logger"
    _settings: "KafkaSettings"

    async def produce(self: Self, message: bytes) -> None:
        """Отправить сообщение в топик."""
        producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.bootstrap_servers,
            client_id=self._settings.client_id,
        )
        async with producer as context:
            await context.send_and_wait(self._settings.topic_name, message)
