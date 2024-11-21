from src.container import CONTAINER


async def actualize_config() -> None:
    """Актуализировать конфигурацию."""
    adapter = CONTAINER.config_adapter()

    await adapter.actualize()


async def clean_order_history() -> None:
    """Удалить устаревшие заказы."""
    adapter = CONTAINER.order_adapter()
    settings = CONTAINER.order_settings()

    await adapter.clean(settings.retention)
