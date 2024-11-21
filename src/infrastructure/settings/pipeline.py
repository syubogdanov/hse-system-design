from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    """Настройки пайплайнов."""

    # Максимальное число одновеменно запущенных этапов.
    max_concurrent_stages: PositiveInt = 100

    model_config = SettingsConfigDict(env_prefix="pipeline_")
