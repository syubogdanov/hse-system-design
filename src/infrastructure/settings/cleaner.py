from datetime import timedelta

from pydantic_settings import BaseSettings


class CleanerSettings(BaseSettings):
    """Настройки очистителя."""

    # Периодичность запуска.
    crontab: str = "* * * * *"
    # Наибольший возраст данных.
    retention: timedelta = timedelta(days=365)
