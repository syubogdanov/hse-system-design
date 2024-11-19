from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class TaskSettings(BaseSettings):
    """Настройки задач."""

    # Число одновременно обрабатываемых задач.
    max_concurrent_tasks: PositiveInt = 25

    model_config = SettingsConfigDict(env_prefix="task_")
