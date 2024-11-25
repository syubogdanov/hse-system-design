from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import UUID

from httpx import ConnectError, ConnectTimeout
from sqlalchemy.sql import exists, select

from autoclients.performer_stub_client.api.performers import (
    get_nearest_api_v1_performers_nearest_get,
)
from autoclients.performer_stub_client.client import Client
from src.domain.entities.performer import Performer
from src.domain.services.interfaces.performer import PerformerInterface
from src.infrastructure.adapters.constants import retry_database, retry_external_api
from src.infrastructure.models.delivery import DeliveryModel


if TYPE_CHECKING:
    from logging import Logger

    from src.infrastructure.settings.performer import PerformerSettings
    from utils.typing import SessionFactory


@dataclass
class PerformerAdapter(PerformerInterface):
    """Адаптер исполнителя."""

    _logger: "Logger"
    _session_factory: "SessionFactory"
    _settings: "PerformerSettings"

    _delivery_model: ClassVar = DeliveryModel

    @retry_database
    async def is_busy(self: Self, performer_id: UUID) -> bool:
        """Получить пайплайн по идентификатору."""
        subquery = exists().where(
            self._delivery_model == performer_id,
            self._delivery_model.released_at.is_not(None),
        )

        async with self._session_factory() as session:
            query_result = await session.execute(select(subquery))
            return bool(query_result.scalar())

    @retry_external_api
    async def get_nearest(self: Self, zone_id: UUID) -> list["Performer"]:
        """Получить свободных исполнителей."""
        try:
            response = await get_nearest_api_v1_performers_nearest_get.asyncio_detailed(
                client=Client(self._settings.service_url, raise_on_unexpected_status=True),
                zone_id=zone_id,
            )

        except ConnectError as exception:
            detail = "The connection to the service could not be established"
            raise ConnectionError(detail) from exception

        except ConnectTimeout as exception:
            detail = "The service did not respond in the allotted time"
            raise TimeoutError(detail) from exception

        except Exception as exception:
            detail = "An unexpected exception occurred"
            raise RuntimeError(detail) from exception

        if response.status_code != HTTPStatus.OK:
            detail = "The request was not successful'"
            raise RuntimeError(detail)

        return [
            Performer.model_validate(model)
            for model in response.parsed
        ]

    @asynccontextmanager
    async def lock(self: Self, performer_id: UUID) -> AsyncGenerator[None, None]:
        """Заблокировать назначение исполнителя на заказы."""
        yield
