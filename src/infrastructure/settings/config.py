from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    """Настройки конфигурации."""

    # URL сервиса.
    service_url: str

    # Расписание актуализации.
    crontab: str = "* * * * *"

    model_config = SettingsConfigDict(env_prefix="config_")
