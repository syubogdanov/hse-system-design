from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Provider, Singleton

from src.domain.entities.pipeline import PipelineName
from src.domain.services.launchers.pipeline import PipelineLauncher
from src.domain.services.pipelines.assign import AssignmentPipeline
from src.domain.services.pipelines.cancel import CancellationPipeline
from src.domain.services.pipelines.estimate import EstimationPipeline
from src.domain.services.pipelines.finish import FinishingPipeline
from src.domain.services.pipelines.start import StartingPipeline
from src.infrastructure.adapters.cleaner import CleanerAdapter
from src.infrastructure.adapters.configuration import ConfigurationAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.settings.cleaner import CleanerSettings
from src.infrastructure.settings.configuration import ConfigurationSettings
from src.infrastructure.settings.logging import LoggingSettings
from utils.logging import get_logger


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.cleaner import CleanerInterface
    from src.domain.services.interfaces.configuration import ConfigurationInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.pipelines.base import BasePipeline


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    cleaner_settings: Provider["CleanerSettings"] = Singleton(CleanerSettings)
    configuration_settings: Provider["ConfigurationSettings"] = Singleton(ConfigurationSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)

    logger: Provider["Logger"] = Singleton(get_logger, level=logging_settings.provided.level)

    assignment_pipeline: Provider["BasePipeline"] = Singleton(
        AssignmentPipeline,
        _logger=logger.provided,
    )
    cancellation_pipeline: Provider["BasePipeline"] = Singleton(
        CancellationPipeline,
        _logger=logger.provided,
    )
    estimation_pipeline: Provider["BasePipeline"] = Singleton(
        EstimationPipeline,
        _logger=logger.provided,
    )
    finishing_pipeline: Provider["BasePipeline"] = Singleton(
        FinishingPipeline,
        _logger=logger.provided,
    )
    starting_pipeline: Provider["BasePipeline"] = Singleton(
        StartingPipeline,
        _logger=logger.provided,
    )

    cleaner_adapter: Provider["CleanerInterface"] = Singleton(
        CleanerAdapter,
        _logger=logger.provided,
    )
    configuration_adapter: Provider["ConfigurationInterface"] = Singleton(
        ConfigurationAdapter,
        _logger=logger.provided,
    )
    trigger_adapter: Provider["TriggerInterface"] = Singleton(
        TriggerAdapter,
        _logger=logger.provided,
    )

    next_pipelines: Provider[dict[PipelineName, PipelineName]] = Dict(
        {
            PipelineName.START: PipelineName.ESTIMATE,
            PipelineName.ESTIMATE: PipelineName.ASSIGN,
        },
    )
    runners: Provider[dict[PipelineName, "BasePipeline"]] = Dict(
        {
            PipelineName.ASSIGN: assignment_pipeline.provided,
            PipelineName.CANCEL: cancellation_pipeline.provided,
            PipelineName.ESTIMATE: estimation_pipeline.provided,
            PipelineName.FINISH: finishing_pipeline.provided,
            PipelineName.START: starting_pipeline.provided,
        },
    )

    pipeline_launcher: Provider["PipelineLauncher"] = Singleton(
        PipelineLauncher,
        _logger=logger.provided,
        _runners=runners.provided,
    )


CONTAINER = Container()
