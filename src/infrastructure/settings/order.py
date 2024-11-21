from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class OrderSettings(BaseSettings):
    """Настройки пайплайнов."""

    # Расписание периодической очистки.
    crontab: str = "* * * * *"
    # Максимальный возраст заказа в истории.
    retention: timedelta = timedelta(days=365)

    model_config = SettingsConfigDict(env_prefix="order_")
