from pydantic_settings import BaseSettings, SettingsConfigDict


class PerformerSettings(BaseSettings):
    """Настройки источника "Исполнители"."""

    # URL сервиса.
    service_url: str

    model_config = SettingsConfigDict(env_prefix="performer_")
