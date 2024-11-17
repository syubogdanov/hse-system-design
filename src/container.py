from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Provider, Singleton

from src.domain.entities.pipeline import PipelineName
from src.domain.services.launchers.pipeline import PipelineLauncher
from src.domain.services.pipelines.assignment import AssignmentPipeline
from src.domain.services.pipelines.cancellation import CancellationPipeline
from src.domain.services.pipelines.estimation import EstimationPipeline
from src.domain.services.pipelines.release import ReleasePipeline
from src.infrastructure.adapters.actualizer import ActualizerAdapter
from src.infrastructure.adapters.cleaner import CleanerAdapter
from src.infrastructure.settings.actualizer import ActualizerSettings
from src.infrastructure.settings.cleaner import CleanerSettings
from src.infrastructure.settings.logging import LoggingSettings
from utils.logging import get_logger


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.actualizer import ActualizerInterface
    from src.domain.services.interfaces.cleaner import CleanerInterface
    from src.domain.services.pipelines.base import BasePipeline


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    actualizer_settings: Provider["ActualizerSettings"] = Singleton(ActualizerSettings)
    cleaner_settings: Provider["CleanerSettings"] = Singleton(CleanerSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)

    logger: Provider["Logger"] = Singleton(get_logger, level=logging_settings.provided.level)

    assignment_pipeline: Provider["AssignmentPipeline"] = Singleton(
        AssignmentPipeline,
        _logger=logger.provided,
    )
    cancellation_pipeline: Provider["CancellationPipeline"] = Singleton(
        CancellationPipeline,
        _logger=logger.provided,
    )
    estimation_pipeline: Provider["EstimationPipeline"] = Singleton(
        EstimationPipeline,
        _logger=logger.provided,
    )
    release_pipeline: Provider["ReleasePipeline"] = Singleton(
        ReleasePipeline,
        _logger=logger.provided,
    )

    runners: Provider[dict[PipelineName, "BasePipeline"]] = Dict(
        {
            PipelineName.ASSIGNMENT: assignment_pipeline.provided,
            PipelineName.CANCELLATION: cancellation_pipeline.provided,
            PipelineName.ESTIMATION: estimation_pipeline.provided,
            PipelineName.RELEASE: release_pipeline.provided,
        },
    )

    pipeline_launcher: Provider["PipelineLauncher"] = Singleton(
        PipelineLauncher,
        _logger=logger.provided,
        _runners=runners.provided,
    )

    actualizer: Provider["ActualizerInterface"] = Singleton(
        ActualizerAdapter,
        _logger=logger.provided,
    )
    cleaner: Provider["CleanerInterface"] = Singleton(CleanerAdapter, _logger=logger.provided)


CONTAINER = Container()
