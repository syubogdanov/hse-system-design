from pydantic_settings import BaseSettings, SettingsConfigDict


class GrpcApiSettings(BaseSettings):
    """Настройки `gRPC` API."""

    # Хост.
    host: str
    # Порт.
    port: int

    model_config = SettingsConfigDict(env_prefix="grpc_api_")
