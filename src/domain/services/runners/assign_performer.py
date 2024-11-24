import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.status import Status
from src.domain.services.exceptions import ExternalServiceError
from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage
    from src.domain.services.interfaces.delivery import DeliveryInterface
    from src.domain.services.interfaces.geography import GeographyInterface
    from src.domain.services.interfaces.order import OrderInterface
    from src.domain.services.interfaces.performer import PerformerInterface
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface


@dataclass
class AssignPerformerRunner(StageRunner):
    """Назначить исполнителя на заказ."""

    _deliveries: "DeliveryInterface"
    _geography: "GeographyInterface"
    _logger: "Logger"
    _orders: "OrderInterface"
    _performers: "PerformerInterface"
    _pipelines: "PipelineInterface"
    _stages: "StageInterface"

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        stage.start()

        _, pipeline, delivery = await asyncio.gather(
            self._stages.update_or_create(stage),
            self._pipelines.get(stage.pipeline_id),
            self._deliveries.get(stage.pipeline_id),
        )

        order = await self._orders.get(pipeline.order_id)

        try:
            zone = await self._geography.get_zone(order.source_address_id)
            nearest_performers = await self._performers.get_nearest(zone.id)

        except ExternalServiceError:
            message = "Failed to get the geolocation of the performers"
            return await self._finish(stage, Status.FAILED, message)

        if not nearest_performers:
            message = "There are physically no performers in the source zone"
            return await self._finish(stage, Status.FAILED, message)

        for performer in nearest_performers:
            async with self._performers.lock(performer.id):
                if not await self._performers.is_busy(performer.id):
                    delivery.assign(performer.id)
                    await self._deliveries.update_or_create(delivery)
                    break

        if not delivery.is_assigned():
            message = "There are no idle performers in the source zone"
            return await self._finish(stage, Status.FAILED, message)

        return await self._finish(stage, Status.SUCCEEDED)

    async def _finish(
        self: Self,
        stage: "Stage",
        status: Status,
        message: str | None = None,
    ) -> "Stage":
        """Завершить этап."""
        stage.finish(status, message)
        await self._stages.update_or_create(stage)
        return stage
