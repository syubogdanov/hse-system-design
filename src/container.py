from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Dict, Provider, Singleton

from src.domain.entities.stage import StageName
from src.domain.services.launchers.pipeline import PipelineLauncher
from src.domain.services.launchers.stage import StageLauncher
from src.domain.services.runners.assign_performer import AssignPerformerRunner
from src.domain.services.runners.estimate_price import EstimatePriceRunner
from src.domain.services.runners.perform_order import PerformOrderRunner
from src.domain.services.runners.release_performer import ReleasePerformerRunner
from src.domain.services.runners.start_pipeline import StartPipelineRunner
from src.infrastructure.adapters.config import ConfigAdapter
from src.infrastructure.adapters.pipeline import PipelineAdapter
from src.infrastructure.adapters.stage import StageAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.logging.factory import create_logger
from src.infrastructure.settings.config import ConfigSettings
from src.infrastructure.settings.database import DatabaseSettings
from src.infrastructure.settings.grpc_api import GrpcApiSettings
from src.infrastructure.settings.http_api import HttpApiSettings
from src.infrastructure.settings.kafka import KafkaSettings
from src.infrastructure.settings.logging import LoggingSettings
from src.infrastructure.settings.pipeline import PipelineSettings


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.config import ConfigInterface
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import StageRunner


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    config_settings: Provider["ConfigSettings"] = Singleton(ConfigSettings)
    database_settings: Provider["DatabaseSettings"] = Singleton(DatabaseSettings)
    grpc_api_settings: Provider["GrpcApiSettings"] = Singleton(GrpcApiSettings)
    http_api_settings: Provider["HttpApiSettings"] = Singleton(HttpApiSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)
    kafka_settings: Provider["KafkaSettings"] = Singleton(KafkaSettings)
    pipeline_settings: Provider["PipelineSettings"] = Singleton(PipelineSettings)

    logger: Provider["Logger"] = Singleton(
        create_logger,
        format_=logging_settings.provided.format,
        level=logging_settings.provided.level,
    )

    id_factory: Provider[UUID] = Callable(uuid4)

    config_adapter: Provider["ConfigInterface"] = Singleton(
        ConfigAdapter,
        _logger=logger.provided,
    )
    pipeline_adapter: Provider["PipelineInterface"] = Singleton(
        PipelineAdapter,
        _logger=logger.provided,
    )
    stage_adapter: Provider["StageInterface"] = Singleton(
        StageAdapter,
        _logger=logger.provided,
    )
    trigger_adapter: Provider["TriggerInterface"] = Singleton(
        TriggerAdapter,
        _logger=logger.provided,
    )

    assign_performer_runner: Provider["StageRunner"] = Singleton(
        AssignPerformerRunner,
        _logger=logger.provided,
    )
    estimate_price_runner: Provider["StageRunner"] = Singleton(
        EstimatePriceRunner,
        _logger=logger.provided,
    )
    perform_order_runner: Provider["StageRunner"] = Singleton(
        PerformOrderRunner,
        _logger=logger.provided,
    )
    release_performer_runner: Provider["StageRunner"] = Singleton(
        ReleasePerformerRunner,
        _logger=logger.provided,
    )
    start_pipeline_runner: Provider["StageRunner"] = Singleton(
        StartPipelineRunner,
        _logger=logger.provided,
    )

    runners: Provider[dict["StageName", "StageRunner"]] = Dict(
        {
            StageName.ASSIGN_PERFORMER: assign_performer_runner.provided,
            StageName.ESTIMATE_PRICE: estimate_price_runner.provided,
            StageName.PERFORM_ORDER: perform_order_runner.provided,
            StageName.RELEASE_PERFORMER: release_performer_runner.provided,
            StageName.START_PIPELINE: start_pipeline_runner.provided,
        },
    )

    pipeline_launcher: Provider["PipelineLauncher"] = Singleton(
        PipelineLauncher,
        _id_factory=id_factory.provider,
        _logger=logger.provided,
        _pipelines=pipeline_adapter.provided,
        _stages=stage_adapter.provided,
        _triggers=trigger_adapter.provided,
    )
    stage_launcher: Provider["StageLauncher"] = Singleton(
        StageLauncher,
        _id_factory=id_factory.provider,
        _logger=logger.provided,
        _pipelines=pipeline_adapter.provided,
        _runners=runners.provided,
        _stages=stage_adapter.provided,
        _triggers=trigger_adapter.provided,
    )


CONTAINER = Container()
