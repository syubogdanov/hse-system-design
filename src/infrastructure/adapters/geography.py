from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, Self
from uuid import UUID

from httpx import ConnectError, ConnectTimeout

from autoclients.geography_stub_client.api.address import get_zone_api_v1_address_id_zone_get
from autoclients.geography_stub_client.api.math import (
    get_distance_api_v1_math_distance_get,
    get_load_factor_api_v1_math_load_factor_get,
)
from autoclients.geography_stub_client.client import Client
from src.domain.entities.zone import Zone
from src.domain.services.interfaces.geography import GeographyInterface
from src.infrastructure.adapters.constants import retry_external_api


if TYPE_CHECKING:
    from logging import Logger

    from pydantic import NonNegativeFloat

    from src.infrastructure.settings.geography import GeographySettings



@dataclass
class GeographyAdapter(GeographyInterface):
    """Интерфейс географии."""

    _logger: "Logger"
    _settings: "GeographySettings"

    @retry_external_api
    async def get_zone(self: Self, address_id: UUID) -> "Zone":
        """Получить идентификатор области."""
        try:
            response = await get_zone_api_v1_address_id_zone_get.asyncio_detailed(
                client=Client(self._settings.service_url, raise_on_unexpected_status=True),
                id=address_id,
            )

        except ConnectError as exception:
            detail = "The connection to the service could not be established"
            raise ConnectionError(detail) from exception

        except ConnectTimeout as exception:
            detail = "The service did not respond in the allotted time"
            raise TimeoutError(detail) from exception

        except Exception as exception:
            detail = "An unexpected exception occurred"
            raise OSError(detail) from exception

        if response.status_code != HTTPStatus.OK:
            detail = "The request was not successful'"
            raise RuntimeError(detail)

        return Zone.model_validate(response.parsed)

    @retry_external_api
    async def get_load_factor(self: Self, zone_id: UUID) -> "NonNegativeFloat":
        """Получить коэффициент загруженности области."""
        try:
            response = await get_load_factor_api_v1_math_load_factor_get.asyncio_detailed(
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
            raise OSError(detail) from exception

        if response.status_code != HTTPStatus.OK:
            detail = "The request was not successful'"
            raise RuntimeError(detail)

        if not isinstance(response.parsed, float):
            detail = "The response is not 'float'"
            raise TypeError(detail)

        return response.parsed

    @retry_external_api
    async def get_distance(
        self: Self,
        source_address_id: UUID,
        target_address_id: UUID,
    ) -> "NonNegativeFloat":
        """Получить расстояние между адресами."""
        try:
            response = await get_distance_api_v1_math_distance_get.asyncio_detailed(
                client=Client(self._settings.service_url, raise_on_unexpected_status=True),
                source_address_id=source_address_id,
                target_address_id=target_address_id,
            )

        except ConnectError as exception:
            detail = "The connection to the service could not be established"
            raise ConnectionError(detail) from exception

        except ConnectTimeout as exception:
            detail = "The service did not respond in the allotted time"
            raise TimeoutError(detail) from exception

        except Exception as exception:
            detail = "An unexpected exception occurred"
            raise OSError(detail) from exception

        if response.status_code != HTTPStatus.OK:
            detail = "The request was not successful'"
            raise RuntimeError(detail)

        if not isinstance(response.parsed, float):
            detail = "The response is not 'float'"
            raise TypeError(detail)

        return response.parsed
