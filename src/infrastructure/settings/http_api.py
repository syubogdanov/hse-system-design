from pydantic_settings import BaseSettings, SettingsConfigDict


class HttpApiSettings(BaseSettings):
    """Настройки `HTTP` API."""

    # Хост.
    host: str
    # Порт.
    port: int

    model_config = SettingsConfigDict(env_prefix="http_api_")
