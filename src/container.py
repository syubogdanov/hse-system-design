from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton

from src.infrastructure.settings.actualizer import ActualizerSettings
from src.infrastructure.settings.cleaner import CleanerSettings
from src.infrastructure.settings.logging import LoggingSettings
from utils.logging import get_logger


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.actualizer import ActualizerInterface
    from src.domain.services.interfaces.cleaner import CleanerInterface


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    actualizer_settings: Provider["ActualizerSettings"] = Singleton(ActualizerSettings)
    cleaner_settings: Provider["CleanerSettings"] = Singleton(CleanerSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)

    logger: Provider["Logger"] = Singleton(get_logger, level=logging_settings.provided.level)

    actualizer: Provider["ActualizerInterface"] = ...
    cleaner: Provider["CleanerInterface"] = ...


CONTAINER = Container()
