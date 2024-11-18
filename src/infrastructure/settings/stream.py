from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class StreamSettings(BaseSettings):
    """Настройки потока."""

    # Число одновременно обрабатываемых событий.
    max_concurrent_tasks: PositiveInt = 25

    model_config = SettingsConfigDict(env_prefix="stream_")
