from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Provider, Singleton

from src.domain.entities.task import TaskName
from src.domain.services.launchers.trigger import TriggerLauncher
from src.domain.services.runners.assign import AssignmentRunner
from src.domain.services.runners.cancel import CancellationRunner
from src.domain.services.runners.estimate import EstimationRunner
from src.domain.services.runners.finish import FinishingRunner
from src.domain.services.runners.start import StartingRunner
from src.infrastructure.adapters.configuration import ConfigurationAdapter
from src.infrastructure.adapters.job import JobAdapter
from src.infrastructure.adapters.kafka.consumer import KafkaConsumerAdapter
from src.infrastructure.adapters.kafka.producer import KafkaProducerAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.settings.configuration import ConfigurationSettings
from src.infrastructure.settings.job import JobSettings
from src.infrastructure.settings.kafka import KafkaSettings
from src.infrastructure.settings.logging import LoggingSettings
from src.infrastructure.settings.task import TaskSettings
from utils.logging import get_logger


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.configuration import ConfigurationInterface
    from src.domain.services.interfaces.job import JobInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.runners.base import TaskRunner


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    configuration_settings: Provider["ConfigurationSettings"] = Singleton(ConfigurationSettings)
    job_settings: Provider["JobSettings"] = Singleton(JobSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)
    kafka_settings: Provider["KafkaSettings"] = Singleton(KafkaSettings)
    task_settings: Provider["TaskSettings"] = Singleton(TaskSettings)

    logger: Provider["Logger"] = Singleton(get_logger, level=logging_settings.provided.level)

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

    configuration_adapter: Provider["ConfigurationInterface"] = Singleton(
        ConfigurationAdapter,
        _logger=logger.provided,
    )
    job_adapter: Provider["JobInterface"] = Singleton(
        JobAdapter,
        _logger=logger.provided,
    )
    trigger_adapter: Provider["TriggerInterface"] = Singleton(
        TriggerAdapter,
        _logger=logger.provided,
        _producer=kafka_producer.provided,
    )

    assignment_runner: Provider["TaskRunner"] = Singleton(
        AssignmentRunner,
        _jobs=job_adapter.provided,
        _logger=logger.provided,
    )
    cancellation_runner: Provider["TaskRunner"] = Singleton(
        CancellationRunner,
        _jobs=job_adapter.provided,
        _logger=logger.provided,
    )
    estimation_runner: Provider["TaskRunner"] = Singleton(
        EstimationRunner,
        _jobs=job_adapter.provided,
        _logger=logger.provided,
    )
    finishing_runner: Provider["TaskRunner"] = Singleton(
        FinishingRunner,
        _jobs=job_adapter.provided,
        _logger=logger.provided,
    )
    starting_runner: Provider["TaskRunner"] = Singleton(
        StartingRunner,
        _jobs=job_adapter.provided,
        _logger=logger.provided,
    )

    runners: Provider[dict[TaskName, "TaskRunner"]] = Dict(
        {
            TaskName.ASSIGN: assignment_runner.provided,
            TaskName.CANCEL: cancellation_runner.provided,
            TaskName.ESTIMATE: estimation_runner.provided,
            TaskName.FINISH: finishing_runner.provided,
            TaskName.START: starting_runner.provided,
        },
    )

    trigger_launcher: Provider["TriggerLauncher"] = Singleton(
        TriggerLauncher,
        _logger=logger.provided,
        _runners=runners.provided,
        _trigger=trigger_adapter.provided,
    )


CONTAINER = Container()
