class ServiceError(Exception):
    """Ошибка сервиса."""


class ParametersError(ServiceError):
    """Ошибка параметров."""


class TaskError(ServiceError):
    """Ошибка выполнения задачи."""
