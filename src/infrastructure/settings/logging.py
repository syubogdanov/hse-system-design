from logging import INFO

from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Настройки логирования."""

    # Уровень логирования
    level: int = INFO

    model_config = SettingsConfigDict(env_prefix="logging_")
