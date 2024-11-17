from src.container import CONTAINER


async def actualize() -> None:
    """Актуализировать конфигурацию."""
    adapter = CONTAINER.configuration_adapter()

    await adapter.actualize()


async def clean() -> None:
    """Очистить устаревшие данные."""
    adapter = CONTAINER.cleaner_adapter()
    settings = CONTAINER.cleaner_settings()

    await adapter.clean(settings.retention)
