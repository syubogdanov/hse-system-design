from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Provider, Singleton

from src.domain.entities.stage import StageName
from src.domain.services.launchers.trigger import TriggerLauncher
from src.domain.services.runners.assign import AssignRunner
from src.domain.services.runners.estimate import EstimateRunner
from src.domain.services.runners.release import ReleaseRunner
from src.domain.services.runners.start import StartRunner
from src.infrastructure.adapters.config import ConfigAdapter
from src.infrastructure.adapters.kafka.consumer import KafkaConsumerAdapter
from src.infrastructure.adapters.kafka.producer import KafkaProducerAdapter
from src.infrastructure.adapters.pipeline import PipelineAdapter
from src.infrastructure.adapters.stage import StageAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.logging.factory import get_logger
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
        get_logger,
        format_=logging_settings.provided.format,
        level=logging_settings.provided.level,
    )

    kafka_consumer: Provider["KafkaConsumerAdapter"] = Singleton(
        KafkaConsumerAdapter,
        _logger=logger.provided,
        _settings=kafka_settings.provided,
    )
    kafka_producer: Provider["KafkaProducerAdapter"] = Singleton(
        KafkaProducerAdapter,
        _logger=logger.provided,
        _settings=kafka_settings.provided,
    )

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
        _producer=kafka_producer.provided,
    )

    assign_runner: Provider["StageRunner"] = Singleton(
        AssignRunner,
        _logger=logger.provided,
    )
    estimate_runner: Provider["StageRunner"] = Singleton(
        EstimateRunner,
        _logger=logger.provided,
    )
    release_runner: Provider["StageRunner"] = Singleton(
        ReleaseRunner,
        _logger=logger.provided,
    )
    start_runner: Provider["StageRunner"] = Singleton(
        StartRunner,
        _logger=logger.provided,
    )

    runners: Provider[dict["StageName", "StageRunner"]] = Dict(
        {
            StageName.ASSIGN: assign_runner.provided,
            StageName.ESTIMATE: estimate_runner.provided,
            StageName.RELEASE: release_runner.provided,
            StageName.START: start_runner.provided,
        },
    )

    trigger_launcher: Provider["TriggerLauncher"] = Singleton(
        TriggerLauncher,
        _logger=logger.provided,
        _pipelines=pipeline_adapter.provided,
        _runners=runners.provided,
        _stages=stage_adapter.provided,
        _triggers=trigger_adapter.provided,
    )


CONTAINER = Container()
