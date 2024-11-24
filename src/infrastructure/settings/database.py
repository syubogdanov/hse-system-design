from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки базы данных."""

    # Хост.
    host: str
    # Порт.
    port: int

    # Имя пользователя.
    username: str
    # Пароль.
    password: str

    # Название БД.
    name: str

    # Протокол для подключения.
    dialect: str = "postgresql"
    # Драйвер для подключения.
    driver: str = "asyncpg"

    # Автоматически подтверждать транзакции.
    autocommit: bool = False
    # Автоматически отправлять запросы.
    autoflush: bool = False
    # Обновлять объект после фиксации транзакции.
    expire_on_commit: bool = False

    @property
    def url(self: Self) -> str:
        """URL для подключения к БД."""
        protocol = f"{self.dialect}+{self.driver}"
        return f"{protocol}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_prefix="database_")
