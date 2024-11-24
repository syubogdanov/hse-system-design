from pydantic_settings import BaseSettings, SettingsConfigDict


class TopicNameSettings(BaseSettings):
    """Настройки топиков."""

    # Название топика результатов.
    results: str
    # Название топика триггеров.
    triggers: str

    model_config = SettingsConfigDict(env_prefix="topic_name_")
