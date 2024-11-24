from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    """Настройки конфигурации."""

    # Хост.
    host: str
    # Порт.
    port: str

    # Расписание актуализации.
    crontab: str = "* * * * *"

    model_config = SettingsConfigDict(env_prefix="config_")
