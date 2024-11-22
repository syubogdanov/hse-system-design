from http import HTTPStatus

from fastapi.requests import Request
from fastapi.responses import Response


def on_not_found(_request: Request, exception: Exception) -> Response:
    """Ответ на отсутствие данных."""
    return Response(content=str(exception), status_code=HTTPStatus.NOT_FOUND)
