from logging import INFO

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """Настройки логирования."""

    # Уровень логирования
    level: int = INFO
