import asyncio

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.infrastructure.models import *  # noqa: F403
from src.infrastructure.models.base import BaseModel


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations(connection: Connection) -> None:
    """Накатить миграции [синхронно]."""
    context.configure(connection=connection, target_metadata=BaseModel.metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Накатить миграции [асинхронно]."""
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
