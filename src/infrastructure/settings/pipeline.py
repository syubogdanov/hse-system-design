from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    """Настройки пайплайнов."""

    # Максимальное число одновеменно обрабатываемых триггеров.
    max_concurrent_triggers: PositiveInt = 100
    # Максимальное число одновеменно обрабатываемых результатов.
    max_concurrent_results: PositiveInt = 250

    model_config = SettingsConfigDict(env_prefix="pipeline_")
