from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from sqlalchemy import select

from src.domain.entities.config import Config
from src.domain.services.interfaces.config import ConfigInterface
from src.infrastructure.adapters.constants import retry_database, retry_external_api
from src.infrastructure.models.config import ConfigModel


if TYPE_CHECKING:
    from logging import Logger

    from utils.typing import SessionFactory


@dataclass
class ConfigAdapter(ConfigInterface):
    """Адаптер конфигурации."""

    _logger: "Logger"
    _session_factory: "SessionFactory"

    _config_model: ClassVar = ConfigModel

    @retry_external_api
    async def actualize(self: Self) -> None:
        """Актуализировать конфигурацию."""
        raise NotImplementedError

    @retry_database
    async def get(self: Self) -> "Config | None":
        """Получить конфигурацию."""
        query = select(self._config_model).order_by(self._config_model.fetched_at.desc()).limit(1)

        async with self._session_factory() as session:
            query_result = await session.execute(query)
            model = query_result.scalar()

            return Config.model_validate(model) if model is not None else None
