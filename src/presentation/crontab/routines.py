from src.container import CONTAINER


async def actualize_configuration() -> None:
    """Актуализировать конфигурацию."""
    adapter = CONTAINER.configuration_adapter()

    await adapter.actualize()


async def clean_jobs() -> None:
    """Удалить устаревшие работы."""
    adapter = CONTAINER.job_adapter()
    settings = CONTAINER.job_settings()

    await adapter.clean(settings.retention)
