from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize_configuration, cleanup


class CrontabLauncher:
    """Кронтаб лаунчер."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтабы."""
        loop = get_event_loop()

        cleaner_settings = CONTAINER.cleaner_settings()
        configuration_settings = CONTAINER.configuration_settings()

        crontab(configuration_settings.crontab, actualize_configuration, loop=loop)
        crontab(cleaner_settings.crontab, cleanup, loop=loop)

        loop.run_forever()
