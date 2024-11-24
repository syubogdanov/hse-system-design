from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    # Название проекта.
    name: str = "Geography Stub"

    model_config = SettingsConfigDict(env_prefix="app_")
