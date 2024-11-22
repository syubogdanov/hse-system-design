from http import HTTPStatus

from fastapi.requests import Request
from fastapi.responses import Response


def on_not_found_error(_request: Request, exception: Exception) -> Response:
    """Ответ на отсутствие данных."""
    return Response(content=str(exception), status_code=HTTPStatus.NOT_FOUND)


def on_stage_error(_request: Request, exception: Exception) -> Response:
    """Ответ на отсутствие данных."""
    return Response(content=str(exception), status_code=HTTPStatus.BAD_REQUEST)


def on_pipeline_error(_request: Request, exception: Exception) -> Response:
    """Ответ на отсутствие данных."""
    return Response(content=str(exception), status_code=HTTPStatus.BAD_REQUEST)
