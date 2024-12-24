import asyncio

from logging.config import fileConfig
from typing import TYPE_CHECKING

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.infrastructure.models import *  # noqa: F403
from src.infrastructure.models.base import BaseModel
from src.infrastructure.settings.database import DatabaseSettings


if TYPE_CHECKING:
    from alembic.config import Config


def get_settings() -> "DatabaseSettings":
    """Получить настройки БД."""
    return DatabaseSettings()


def get_config() -> "Config":
    """Получить конфиг."""
    config = context.config

    if config.config_file_name:
        fileConfig(config.config_file_name)

    settings = get_settings()

    config.set_main_option("sqlalchemy.url", settings.url)

    return config


def run_migrations(connection: Connection) -> None:
    """Накатить миграции [синхронно]."""
    context.configure(connection=connection, target_metadata=BaseModel.metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Накатить миграции [асинхронно]."""
    config = get_config()

    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        await connection.run_sync(run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    detail = "The offline mode is not supported"
    raise RuntimeError(detail)


asyncio.run(run_async_migrations())
