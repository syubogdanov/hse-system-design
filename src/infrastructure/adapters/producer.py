from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, SupportsBytes

from aiokafka.producer import AIOKafkaProducer

from src.infrastructure.adapters.constants import retry_kafka


if TYPE_CHECKING:
    from logging import Logger

    from src.infrastructure.settings.kafka import KafkaSettings


@dataclass
class KafkaProducerAdapter:
    """Адаптер продюсера `Kafka`."""

    _logger: "Logger"
    _settings: "KafkaSettings"

    def __post_init__(self: Self) -> None:
        """Дополнительная инициализация объекта."""
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.bootstrap_servers,
            client_id=self._settings.client_id,
        )

    @retry_kafka
    async def produce(self: Self, topic_name: str, event: SupportsBytes) -> None:
        """Отправить сообщение в топик."""
        async with self._producer as context:
            await context.send_and_wait(topic_name, bytes(event))
