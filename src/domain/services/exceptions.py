class ServiceError(Exception):
    """Ошибка сервиса."""


class NotFoundError(ServiceError):
    """Ошибка отсутствия данных."""


class ParametersError(ServiceError):
    """Ошибка параметризации."""


class TaskError(ServiceError):
    """Ошибка выполнения задачи."""
