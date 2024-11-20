from src.container import CONTAINER


async def actualize_configuration() -> None:
    """Актуализировать конфигурацию."""
    adapter = CONTAINER.config_adapter()

    await adapter.actualize()


async def clean_pipeline_history() -> None:
    """Удалить устаревшие пайплайны."""
    adapter = CONTAINER.pipeline_adapter()
    settings = CONTAINER.pipeline_settings()

    await adapter.clean(settings.retention)
