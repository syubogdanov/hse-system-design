from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class CleanerSettings(BaseSettings):
    """Настройки очистителя."""

    # Периодичность очистки.
    crontab: str = "* * * * *"
    # Максимально допустимый возраст данных.
    retention: timedelta = timedelta(days=365)

    model_config = SettingsConfigDict(env_prefix="cleaner_")
