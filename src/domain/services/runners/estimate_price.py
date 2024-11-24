import asyncio

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from src.domain.entities.status import Status
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
class EstimatePriceRunner(StageRunner):
    """Оценить стоимость выполнения заказа."""

    _configs: "ConfigInterface"
    _deliveries: "DeliveryInterface"
    _geography: "GeographyInterface"
    _logger: "Logger"
    _orders: "OrderInterface"
    _pipelines: "PipelineInterface"
    _stages: "StageInterface"

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

        distance, source_zone_id = await asyncio.gather(
            self._geography.get_distance(order.source_address_id, order.target_address_id),
            self._geography.get_zone(order.source_address_id),
        )
        load_factor = await self._geography.get_load_factor(source_zone_id)

        calculated_price = distance * config.rubles_per_meter * load_factor
        price = max(config.min_price, calculated_price)

        delivery = await self._deliveries.get(pipeline.id)
        delivery.estimate(price)

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
