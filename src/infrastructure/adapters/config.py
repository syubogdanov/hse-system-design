from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, ClassVar, Self

from httpx import ConnectError, ConnectTimeout
from sqlalchemy import delete, select

from autoclients.config_stub_client.api.configs import get_latest_api_v1_configs_latest_get
from autoclients.config_stub_client.client import Client
from src.domain.entities.config import Config
from src.domain.services.interfaces.config import ConfigInterface
from src.infrastructure.adapters.constants import retry_database, retry_external_api
from src.infrastructure.models.config import ConfigModel


if TYPE_CHECKING:
    from logging import Logger

    from src.infrastructure.settings.config import ConfigSettings
    from utils.typing import SessionFactory


@dataclass
class ConfigAdapter(ConfigInterface):
    """Адаптер конфигурации."""

    _logger: "Logger"
    _session_factory: "SessionFactory"
    _settings: "ConfigSettings"

    # Источник не критичный - кэш разрешен
    _cached_config: Config | None = None

    _config_model: ClassVar = ConfigModel

    @retry_external_api
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        try:
            client = Client(self._settings.service_url, raise_on_unexpected_status=True)
            response = await get_latest_api_v1_configs_latest_get.asyncio_detailed(client=client)

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

        self._cached_config = Config.model_validate(response.parsed)
        model = self._config_model(**self._cached_config.model_dump())

        delete_query = delete(self._config_model)

        async with self._session_factory() as session:
            await session.execute(delete_query)
            session.add(model)

    @retry_database
    async def get(self: Self) -> "Config | None":
        """Получить конфигурацию."""
        if self._cached_config:
            return self._cached_config

        query = select(self._config_model).order_by(self._config_model.fetched_at.desc()).limit(1)

        async with self._session_factory() as session:
            query_result = await session.execute(query)
            model = query_result.scalar()

            return Config.model_validate(model) if model is not None else None
