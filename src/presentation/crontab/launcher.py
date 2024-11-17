from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize, clean


class CrontabLauncher:
    """Кронтаб лаунчер."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтабы."""
        loop = get_event_loop()

        actualizer_settings = CONTAINER.actualizer_settings()
        cleaner_settings = CONTAINER.cleaner_settings()

        crontab(actualizer_settings.crontab, actualize, loop=loop)
        crontab(cleaner_settings.crontab, clean, loop=loop)

        loop.run_forever()
