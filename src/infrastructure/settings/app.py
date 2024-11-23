from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.pyproject import get_version


class AppSettings(BaseSettings):
    """Настройки конфигурации."""

    # Название проекта.
    name: str = "Sorting Hat"
    # Версия проекта.
    version: str = Field(default_factory=get_version)

    model_config = SettingsConfigDict(env_prefix="app_")
