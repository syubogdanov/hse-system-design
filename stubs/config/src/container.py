from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton

from src.infrastructure.adapters.config import ConfigAdapter
from src.infrastructure.settings.app import AppSettings
from src.infrastructure.settings.http_api import HttpApiSettings


if TYPE_CHECKING:
    from src.domain.services.interfaces.config import ConfigInterface


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    app_settings: Provider["AppSettings"] = Singleton(AppSettings)
    http_api_settings: Provider["HttpApiSettings"] = Singleton(HttpApiSettings)

    config_adapter: Provider["ConfigInterface"] = Singleton(ConfigAdapter)


CONTAINER = Container()
