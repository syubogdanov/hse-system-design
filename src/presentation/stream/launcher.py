from typing import Self


class StreamLauncher:
    """Лаунчер потока."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить поток."""
        raise NotImplementedError
