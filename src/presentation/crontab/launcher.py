from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize_config, clean_order_history


class CrontabLauncher:
    """Лаунчер кронтаб-задач."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтабы."""
        logger = CONTAINER.logger()

        config_settings = CONTAINER.config_settings()
        order_settings = CONTAINER.order_settings()

        loop = get_event_loop()

        crontab(config_settings.crontab, actualize_config, loop=loop)
        crontab(order_settings.crontab, clean_order_history, loop=loop)

        logger.info("Starting the crontab...")

        loop.run_forever()
