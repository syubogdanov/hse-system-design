from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Provider, Singleton

from src.domain.entities.task import TaskName
from src.domain.services.launchers.task import TaskLauncher
from src.domain.services.tasks.assign import AssignmentTask
from src.domain.services.tasks.cancel import CancellationTask
from src.domain.services.tasks.estimate import EstimationTask
from src.domain.services.tasks.finish import FinishingTask
from src.domain.services.tasks.start import StartingTask
from src.infrastructure.adapters.cleaner import CleanerAdapter
from src.infrastructure.adapters.configuration import ConfigurationAdapter
from src.infrastructure.adapters.kafka.consumer import KafkaConsumerAdapter
from src.infrastructure.adapters.kafka.producer import KafkaProducerAdapter
from src.infrastructure.adapters.trigger import TriggerAdapter
from src.infrastructure.settings.cleaner import CleanerSettings
from src.infrastructure.settings.configuration import ConfigurationSettings
from src.infrastructure.settings.kafka import KafkaSettings
from src.infrastructure.settings.logging import LoggingSettings
from src.infrastructure.settings.stream import StreamSettings
from utils.logging import get_logger


if TYPE_CHECKING:
    from logging import Logger

    from src.domain.services.interfaces.cleaner import CleanerInterface
    from src.domain.services.interfaces.configuration import ConfigurationInterface
    from src.domain.services.interfaces.trigger import TriggerInterface
    from src.domain.services.tasks.base import TaskRunner


class Container(DeclarativeContainer):
    """Контейнер зависимостей."""

    cleaner_settings: Provider["CleanerSettings"] = Singleton(CleanerSettings)
    configuration_settings: Provider["ConfigurationSettings"] = Singleton(ConfigurationSettings)
    logging_settings: Provider["LoggingSettings"] = Singleton(LoggingSettings)
    kafka_settings: Provider["KafkaSettings"] = Singleton(KafkaSettings)
    stream_settings: Provider["StreamSettings"] = Singleton(StreamSettings)

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

    assignment_task: Provider["TaskRunner"] = Singleton(
        AssignmentTask,
        _logger=logger.provided,
    )
    cancellation_task: Provider["TaskRunner"] = Singleton(
        CancellationTask,
        _logger=logger.provided,
    )
    estimation_task: Provider["TaskRunner"] = Singleton(
        EstimationTask,
        _logger=logger.provided,
    )
    finishing_task: Provider["TaskRunner"] = Singleton(
        FinishingTask,
        _logger=logger.provided,
    )
    starting_task: Provider["TaskRunner"] = Singleton(
        StartingTask,
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
        _producer=kafka_producer.provided,
    )

    next_tasks: Provider[dict[TaskName, TaskName]] = Dict(
        {
            TaskName.START: TaskName.ESTIMATE,
            TaskName.ESTIMATE: TaskName.ASSIGN,
        },
    )
    runners: Provider[dict[TaskName, "TaskRunner"]] = Dict(
        {
            TaskName.ASSIGN: assignment_task.provided,
            TaskName.CANCEL: cancellation_task.provided,
            TaskName.ESTIMATE: estimation_task.provided,
            TaskName.FINISH: finishing_task.provided,
            TaskName.START: starting_task.provided,
        },
    )

    task_launcher: Provider["TaskLauncher"] = Singleton(
        TaskLauncher,
        _logger=logger.provided,
        _runners=runners.provided,
        _next_tasks=next_tasks.provided,
        _trigger=trigger_adapter.provided,
    )


CONTAINER = Container()
