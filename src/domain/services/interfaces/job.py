from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from datetime import timedelta
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.job import Job


class JobInterface(Protocol):
    """Интерфейс работы."""

    @abstractmethod
    async def exists(self: Self, id_: UUID) -> bool:
        """Проверить, существует ли работа."""

    @abstractmethod
    async def get(self: Self, id_: UUID) -> "Job":
        """Получить работу по идентификатору."""

    @abstractmethod
    async def update_or_create(self: Self, job: "Job") -> None:
        """Обновить или сохранить работу."""

    @abstractmethod
    def lock(self: Self, id_: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение задач по работе."""

    @abstractmethod
    async def clean(self: Self, retention: timedelta) -> None:
        """Очистить устаревшие данные."""
