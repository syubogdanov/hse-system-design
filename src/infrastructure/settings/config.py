from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    """Настройки конфигурации."""

    # Расписание актуализации.
    crontab: str = "* * * * *"

    model_config = SettingsConfigDict(env_prefix="config_")
