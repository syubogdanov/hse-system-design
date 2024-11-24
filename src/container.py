from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Dict, Provider, Singleton
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from src.domain.entities.stage import StageName
from src.domain.services.launchers.pipeline import PipelineLauncher
from src.domain.services.launchers.stage import StageLauncher
from src.domain.services.runners.assign_performer import AssignPerformerRunner
from src.domain.services.runners.estimate_cost import EstimateCostRunner
from src.domain.services.runners.perform_delivery import PerformDeliveryRunner
from src.domain.services.runners.release_performer import ReleasePerformerRunner
from src.domain.services.runners.start_pipeline import StartPipelineRunner
from src.infrastructure.adapters.config import ConfigAdapter
from src.infrastructure.adapters.consumer import KafkaConsumerAdapter
from src.infrastructure.adapters.delivery import DeliveryAdapter
from src.infrastructure.adapters.geography import GeographyAdapter
from src.infrastructure.adapters.order import OrderAdapter
from src.infrastructure.adapters.performer import PerformerAdapter
from src.infrastructure.adapters.pipeline import PipelineAdapter
from src.infrastructure.adapters.producer import KafkaProducerAdapter
from src.infrastructure.adapters.stage import StageAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.logging.factory import create_logger
from src.infrastructure.settings.app import AppSettings
from src.infrastructure.settings.config import ConfigSettings
from src.infrastructure.settings.database import DatabaseSettings
from src.infrastructure.settings.geography import GeographySettings
from src.infrastructure.settings.grpc_api import GrpcApiSettings
from src.infrastructure.settings.http_api import HttpApiSettings
from src.infrastructure.settings.kafka import KafkaSettings
from src.infrastructure.settings.logging import LoggingSettings
from src.infrastructure.settings.order import OrderSettings
from src.infrastructure.settings.pipeline import PipelineSettings
from src.infrastructure.settings.topic_name import TopicNameSettings


if TYPE_CHECKING:
    from logging import Logger

    from sqlalchemy.ext.asyncio.engine import AsyncEngine
    from sqlalchemy.ext.asyncio.session import AsyncSession

    from src.domain.services.interfaces.config import ConfigInterface
    from src.domain.services.interfaces.delivery import DeliveryInterface
    from src.domain.services.interfaces.geography import GeographyInterface
    from src.domain.services.interfaces.order import OrderInterface
    from src.domain.services.interfaces.performer import PerformerInterface
    from src.domain.services.interfaces.pipeline import PipelineInterface
    from src.domain.services.interfaces.stage import StageInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import StageRunner


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    app_settings: Provider["AppSettings"] = Singleton(AppSettings)
    config_settings: Provider["ConfigSettings"] = Singleton(ConfigSettings)
    database_settings: Provider["DatabaseSettings"] = Singleton(DatabaseSettings)
    geography_settings: Provider["GeographySettings"] = Singleton(GeographySettings)
    grpc_api_settings: Provider["GrpcApiSettings"] = Singleton(GrpcApiSettings)
    http_api_settings: Provider["HttpApiSettings"] = Singleton(HttpApiSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)
    kafka_settings: Provider["KafkaSettings"] = Singleton(KafkaSettings)
    order_settings: Provider["OrderSettings"] = Singleton(OrderSettings)
    pipeline_settings: Provider["PipelineSettings"] = Singleton(PipelineSettings)
    topic_name_settings: Provider["TopicNameSettings"] = Singleton(TopicNameSettings)

    logger: Provider["Logger"] = Singleton(
        create_logger,
        format_=logging_settings.provided.format,
        level=logging_settings.provided.level,
    )

    id_factory: Provider[UUID] = Callable(uuid4)

    engine: Provider["AsyncEngine"] = Singleton(
        create_async_engine,
        url=database_settings.provided.url,
    )
    session_maker: Provider["async_sessionmaker"] = Singleton(
        async_sessionmaker,
        bind=engine.provided,
        autoflush=database_settings.provided.autoflush,
        autocommit=database_settings.provided.autocommit,
        expire_on_commit=database_settings.provided.expire_on_commit,
    )
    session_factory: Provider[AbstractAsyncContextManager["AsyncSession"]] = Callable(
        session_maker.provided.begin,
    )

    kafka_consumer_adapter: Provider["KafkaConsumerAdapter"] = Singleton(
        KafkaConsumerAdapter,
        _logger=logger.provided,
        _settings=kafka_settings.provided,
    )
    kafka_producer_adapter: Provider["KafkaProducerAdapter"] = Singleton(
        KafkaProducerAdapter,
        _logger=logger.provided,
        _settings=kafka_settings.provided,
    )

    config_adapter: Provider["ConfigInterface"] = Singleton(
        ConfigAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
        _settings=config_settings.provided,
    )
    delivery_adapter: Provider["DeliveryInterface"] = Singleton(
        DeliveryAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
    )
    geography_adapter: Provider["GeographyInterface"] = Singleton(
        GeographyAdapter,
        _logger=logger.provided,
        _settings=geography_settings.provided,
    )
    order_adapter: Provider["OrderInterface"] = Singleton(
        OrderAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
    )
    performer_adapter: Provider["PerformerInterface"] = Singleton(
        PerformerAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
    )
    pipeline_adapter: Provider["PipelineInterface"] = Singleton(
        PipelineAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
    )
    stage_adapter: Provider["StageInterface"] = Singleton(
        StageAdapter,
        _logger=logger.provided,
        _session_factory=session_factory.provided,
    )
    trigger_adapter: Provider["TriggerInterface"] = Singleton(
        TriggerAdapter,
        _logger=logger.provided,
        _producer=kafka_producer_adapter.provided,
        _topic_name=topic_name_settings.provided.triggers,
    )

    assign_performer_runner: Provider["StageRunner"] = Singleton(
        AssignPerformerRunner,
        _deliveries=delivery_adapter.provided,
        _geography=geography_adapter.provided,
        _logger=logger.provided,
        _orders=order_adapter.provided,
        _performers=performer_adapter.provided,
        _pipelines=pipeline_adapter.provided,
        _stages=stage_adapter.provided,
    )
    estimate_cost_runner: Provider["StageRunner"] = Singleton(
        EstimateCostRunner,
        _configs=config_adapter.provided,
        _deliveries=delivery_adapter.provided,
        _geography=geography_adapter.provided,
        _logger=logger.provided,
        _orders=order_adapter.provided,
        _pipelines=pipeline_adapter.provided,
        _stages=stage_adapter.provided,
    )
    perform_delivery_runner: Provider["StageRunner"] = Singleton(
        PerformDeliveryRunner,
        _logger=logger.provided,
        _stages=stage_adapter.provided,
    )
    release_performer_runner: Provider["StageRunner"] = Singleton(
        ReleasePerformerRunner,
        _deliveries=delivery_adapter.provided,
        _logger=logger.provided,
        _stages=stage_adapter.provided,
    )
    start_pipeline_runner: Provider["StageRunner"] = Singleton(
        StartPipelineRunner,
        _deliveries=delivery_adapter.provided,
        _logger=logger.provided,
        _pipelines=pipeline_adapter.provided,
        _stages=stage_adapter.provided,
    )

    runners: Provider[dict["StageName", "StageRunner"]] = Dict(
        {
            StageName.ASSIGN_PERFORMER: assign_performer_runner.provided,
            StageName.ESTIMATE_COST: estimate_cost_runner.provided,
            StageName.PERFORM_DELIVERY: perform_delivery_runner.provided,
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
