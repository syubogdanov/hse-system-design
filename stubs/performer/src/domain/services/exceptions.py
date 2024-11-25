class ServiceError(Exception):
    """Ошибка сервиса."""


class NotFoundError(ServiceError):
    """Ошибка отсутствия данных."""
