from socket import gethostname

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    """Настройки `Kafka`."""

    # Список брокеров через запятую.
    bootstrap_servers: str

    # Идентификатор группы.
    group_id: str
    # Идентфикатор клиента.
    client_id: str = Field(default_factory=gethostname)

    # Название топика.
    topic_name: str

    model_config = SettingsConfigDict(env_prefix="kafka_")
