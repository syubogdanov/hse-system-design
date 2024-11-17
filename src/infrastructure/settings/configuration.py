from pydantic_settings import BaseSettings


class ConfigurationSettings(BaseSettings):
    """Настройки конфигурации."""

    # Периодичность актуализации.
    crontab: str = "* * * * *"
