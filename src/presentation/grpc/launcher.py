from typing import Self


class GrpcApiLauncher:
    """Лаунчер `gRPC` API."""

    @classmethod
    def launch(cls: type[Self]) -> None:
        """Запустить `gRPC` API."""
        raise NotImplementedError
