from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.pipeline import PipelineName
from src.domain.exceptions import PipelineError
from src.domain.services.pipelines.base import BasePipeline


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger


@dataclass
class ReleasePipeline(BasePipeline):
    """Пайплайн освобождения исполнителя."""

    _logger: "Logger"

    _pipeline: ClassVar[str] = PipelineName.RELEASE

    async def run(self: Self, trigger: "Trigger") -> None:
        """Запустить пайплайн."""
        if trigger.pipeline != self._pipeline:
            raise PipelineError(Message.WRONG_PIPELINE)

        ...
