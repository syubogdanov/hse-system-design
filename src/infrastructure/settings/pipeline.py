from datetime import timedelta

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    """Настройки пайплайнов."""

    # Расписание периодической очистки.
    crontab: str = "* * * * *"
    # Максимальный возраст пайплайнов в истории.
    retention: timedelta = timedelta(days=365)

    # Максимальное число одновеменно запущенных этапов.
    max_concurrent_stages: PositiveInt = 100

    model_config = SettingsConfigDict(env_prefix="pipeline_")
