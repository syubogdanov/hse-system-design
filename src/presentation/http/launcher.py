from typing import Self

import uvicorn

from src.container import CONTAINER
from src.presentation.http.factory import create_app


class HttpApiLauncher:
    """Лаунчер `HTTP` API."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить `HTTP` API."""
        logger = CONTAINER.logger()
        settings = CONTAINER.http_api_settings()

        app = create_app()

        logger.info("Starting the HTTP API...")

        uvicorn.run(app, host=settings.host, port=settings.port)
