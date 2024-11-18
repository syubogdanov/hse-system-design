from collections.abc import AsyncIterable, Callable, Coroutine
from typing import Any, TypeVar


T = TypeVar("T")


async def aiomap(
    func: Callable[[T], Coroutine[Any, Any, None]],
    iterable: AsyncIterable[T],
    max_concurrent_tasks: int = 1,
) -> None:
    """Применить функцию к итерирумому объекту."""
    raise NotImplementedError
