import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.status import Status
from src.domain.services.exceptions import ExternalServiceError
from src.domain.services.runners.base import StageRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.stage import Stage
    from src.domain.services.interfaces.config import ConfigInterface
    from src.domain.services.interfaces.delivery import DeliveryInterface
    from src.domain.services.interfaces.geography import GeographyInterface
    from src.domain.services.interfaces.order import OrderInterface
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface


@dataclass
class EstimateCostRunner(StageRunner):
    """Оценить стоимость выполнения заказа."""

    _configs: "ConfigInterface"
    _deliveries: "DeliveryInterface"
    _geography: "GeographyInterface"
    _logger: "Logger"
    _orders: "OrderInterface"
    _pipelines: "PipelineInterface"
    _stages: "StageInterface"

    _precision: ClassVar[int] = 2

    async def run(self: Self, stage: "Stage") -> "Stage":
        """Запустить выполнение этапа."""
        stage.start()

        _, config = await asyncio.gather(
            self._stages.update_or_create(stage),
            self._configs.get(),
        )

        if not config:
            message = "Failed to fetch the actual configuration"
            return await self._finish(stage, Status.FAILED, message)

        pipeline = await self._pipelines.get(stage.pipeline_id)
        order = await self._orders.get(pipeline.order_id)

        try:
            distance, source_zone = await asyncio.gather(
                self._geography.get_distance(order.source_address_id, order.target_address_id),
                self._geography.get_zone(order.source_address_id),
            )
            load_factor = await self._geography.get_load_factor(source_zone.id)

        except ExternalServiceError:
            message = "Information on the geography of the order could not be obtained"
            return await self._finish(stage, Status.FAILED, message)

        calculated_cost = distance * config.rubles_per_meter * load_factor
        cost = round(max(config.min_cost, calculated_cost), self._precision)

        delivery = await self._deliveries.get(pipeline.id)
        delivery.estimate(cost)

        _, stage = await asyncio.gather(
            self._deliveries.update_or_create(delivery),
            self._finish(stage, Status.SUCCEEDED),
        )

        return stage

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
