from typing import ClassVar, Self

from alembic import command

from src.container import CONTAINER
from utils.alembic import get_config


class MigrationsLauncher:
    """Лаунчер миграций."""

    _revision: ClassVar[str] = "head"

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить миграции."""
        settings = CONTAINER.database_settings()

        config = get_config(settings.url)
        command.upgrade(config, revision=cls._revision)
