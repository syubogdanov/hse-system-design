from typing import Self


class HttpApiLauncher:
    """Лаунчер `HTTP` API."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить `HTTP` API."""
        raise NotImplementedError
