from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigurationSettings(BaseSettings):
    """Настройки конфигурации."""

    # Периодичность актуализации.
    crontab: str = "* * * * *"

    model_config = SettingsConfigDict(env_prefix="configuration_")
