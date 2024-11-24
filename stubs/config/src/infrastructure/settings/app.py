from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    # Название проекта.
    name: str = "Config Stub"

    model_config = SettingsConfigDict(env_prefix="app_")
