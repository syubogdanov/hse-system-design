from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton

from src.infrastructure.adapters.address import AddressAdapter
from src.infrastructure.adapters.math import MathAdapter
from src.infrastructure.settings.app import AppSettings
from src.infrastructure.settings.http_api import HttpApiSettings


if TYPE_CHECKING:
    from src.domain.services.interfaces.address import AddressInterface
    from src.domain.services.interfaces.math import MathInterface


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    app_settings: Provider["AppSettings"] = Singleton(AppSettings)
    http_api_settings: Provider["HttpApiSettings"] = Singleton(HttpApiSettings)

    math_adapter: Provider["MathInterface"] = Singleton(MathAdapter)
    address_adapter: Provider["AddressInterface"] = Singleton(AddressAdapter)


CONTAINER = Container()
