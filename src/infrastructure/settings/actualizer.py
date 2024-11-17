from pydantic_settings import BaseSettings


class ActualizerSettings(BaseSettings):
    """Настройки актуализатора."""

    # Периодичность запуска.
    crontab: str = "* * * * *"
