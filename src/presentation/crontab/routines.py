from src.container import CONTAINER


async def actualize() -> None:
    """Актуализировать конфигурацию."""
    actualizer = CONTAINER.actualizer()

    await actualizer.actualize()


async def clean() -> None:
    """Очистить устаревшие данные."""
    cleaner = CONTAINER.cleaner()
    settings = CONTAINER.cleaner_settings()

    await cleaner.clean(settings.retention)
