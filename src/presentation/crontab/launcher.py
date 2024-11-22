from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize_config


class CrontabLauncher:
    """Лаунчер кронтаб-задач."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтаб-задачи."""
        logger = CONTAINER.logger()

        config_settings = CONTAINER.config_settings()

        loop = get_event_loop()

        crontab(config_settings.crontab, actualize_config, loop=loop)

        logger.info("Starting the crontab...")

        loop.run_forever()
