from pydantic_settings import BaseSettings, SettingsConfigDict


class GeographySettings(BaseSettings):
    """Настройки источника "Зонирование"."""

    # URL сервиса.
    service_url: str

    model_config = SettingsConfigDict(env_prefix="geography_")
