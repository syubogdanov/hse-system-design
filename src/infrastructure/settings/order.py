from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class OrderSettings(BaseSettings):
    """Настройки заказа."""

    # Расписание очистки истории.
    crontab: str = "* * * * *"
    # Максимальный возраст данных.
    retention: timedelta = timedelta(days=365)

    model_config = SettingsConfigDict(env_prefix="order_")
