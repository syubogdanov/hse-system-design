import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.status import Status
from src.domain.services.exceptions import StageError
from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage
    from src.domain.services.interfaces.delivery import DeliveryInterface
    from src.domain.services.interfaces.stage import StageInterface


@dataclass
class ReleasePerformerRunner(StageRunner):
    """Освободить исполнителя от заказа."""

    _deliveries: "DeliveryInterface"
    _logger: "Logger"
    _stages: "StageInterface"

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        stage.start()

        _, delivery = await asyncio.gather(
            self._stages.update_or_create(stage),
            self._deliveries.get(stage.pipeline_id),
        )

        if not delivery:
            detail = "The delivery does not exist"
            raise StageError(detail, stage)

        delivery.release()

        stage.finish(Status.SUCCEEDED)

        await asyncio.gather(
            self._deliveries.update_or_create(delivery),
            self._stages.update_or_create(stage),
        )

        return stage
