from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.services.interfaces.trigger import TriggerInterface


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger
    from src.infrastructure.adapters.kafka.producer import KafkaProducerAdapter


@dataclass
class TriggerAdapter(TriggerInterface):
    """Адаптер триггер-событий."""

    _logger: "Logger"
    _producer: "KafkaProducerAdapter"

    async def push(self: Self, trigger: "Trigger") -> None:
        """Отправить триггер на выполнение."""
        await self._producer.produce(trigger)
