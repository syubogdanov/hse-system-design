from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class JobSettings(BaseSettings):
    """Настройки работ."""

    # Периодичность очистки.
    clean_crontab: str = "* * * * *"
    # Максимально допустимый возраст данных.
    retention: timedelta = timedelta(days=365)

    model_config = SettingsConfigDict(env_prefix="job_")
