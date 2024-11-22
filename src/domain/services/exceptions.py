class ServiceError(Exception):
    """Ошибка сервиса."""


class PipelineError(ServiceError):
    """Ошибка выполнения пайплайна."""


class StageError(PipelineError):
    """Ошибка выполнения этапа."""


class NotFoundError(Exception):
    """Ошибка отсутствия данных."""
