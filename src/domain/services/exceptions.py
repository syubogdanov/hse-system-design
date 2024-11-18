class ServiceError(Exception):
    """Ошибка сервиса."""


class NotFoundError(ServiceError):
    """Ошибка отсутствия данных."""


class ParametersError(ServiceError):
    """Ошибка параметров."""


class TaskError(ServiceError):
    """Ошибка выполнения задачи."""
