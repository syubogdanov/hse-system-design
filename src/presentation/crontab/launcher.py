from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize_configuration, clean_pipeline_history


class CrontabLauncher:
    """Кронтаб лаунчер."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтабы."""
        config_settings = CONTAINER.config_settings()
        logger = CONTAINER.logger()
        pipeline_settings = CONTAINER.pipeline_settings()

        loop = get_event_loop()

        crontab(config_settings.crontab, actualize_configuration, loop=loop)
        crontab(pipeline_settings.crontab, clean_pipeline_history, loop=loop)

        logger.info("Starting the crontab...")

        loop.run_forever()
