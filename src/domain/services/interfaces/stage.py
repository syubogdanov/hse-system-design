from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Protocol, Self
from uuid import UUID


if TYPE_CHECKING:
    from src.domain.entities.stage import Stage


class StageInterface(Protocol):
    """Интерфейс этапа."""

    @abstractmethod
    async def update_or_create(self: Self, stage: "Stage") -> None:
        """Обновить или сохранить этап."""

    @abstractmethod
    async def get_last_started(self: Self, pipeline_id: UUID) -> "Stage":
        """Получить последний начатый этап."""

    @abstractmethod
    def lock(self: Self, pipeline_id: UUID) -> AbstractAsyncContextManager[None]:
        """Заблокировать выполнение параллельных этапов."""
