from src.container import CONTAINER


async def actualize_config() -> None:
    """Актуализировать конфигурацию."""
    adapter = CONTAINER.config_adapter()

    await adapter.actualize()
