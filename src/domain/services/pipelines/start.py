from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from src.domain.entities.message import Message
from src.domain.entities.pipeline import PipelineName
from src.domain.services.exceptions import ParametersError
from src.domain.services.pipelines.base import PipelineRunner


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.entities.trigger import Trigger


@dataclass
class StartingPipeline(PipelineRunner):
    """Стартовый пайплайн."""

    _logger: "Logger"

    _pipeline: ClassVar[str] = PipelineName.START

    async def run(self: Self, trigger: "Trigger") -> "Trigger":
        """Запустить пайплайн."""
        if trigger.pipeline != self._pipeline:
            raise ParametersError(Message.WRONG_PIPELINE)

        ...
