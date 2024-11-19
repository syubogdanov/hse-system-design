from asyncio.events import get_event_loop

from aiocron import crontab

from src.container import CONTAINER
from src.presentation.crontab.routines import actualize_configuration, clean_jobs


class CrontabLauncher:
    """Кронтаб лаунчер."""

    @staticmethod
    def launch() -> None:
        """Запустить кронтабы."""
        loop = get_event_loop()

        configuration_settings = CONTAINER.configuration_settings()
        job_settings = CONTAINER.job_settings()

        crontab(configuration_settings.crontab, actualize_configuration, loop=loop)
        crontab(job_settings.clean_crontab, clean_jobs, loop=loop)

        loop.run_forever()
