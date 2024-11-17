class ServiceError(Exception):
    """Ошибка сервиса."""


class ParametersError(ServiceError):
    """Ошибка параметров."""


class PipelineError(ServiceError):
    """Ошибка выполнения пайплайна."""
