from asyncio import FIRST_COMPLETED, Task, create_task, wait
from collections.abc import AsyncIterator, Callable, Coroutine
from typing import TYPE_CHECKING, Any, TypeVar


if TYPE_CHECKING:
    from logging import Logger


T = TypeVar("T")
R = TypeVar("R")


async def waitmap(
    function: Callable[[T], Coroutine[Any, Any, R]],
    iterable: AsyncIterator[T],
    *,
    max_concurrent_tasks: int = 1,
    logger: "Logger | None" = None,
) -> None:
    """Применить функцию ко всем объектам итератора.

    Примечания:
        * Исключения не отменяют выполнение других корутин.
    """
    tasks: set[Task] = set()

    def _log_on_exception(task: Task) -> None:
        """Логировать возникновение исключения."""
        if logger is not None and (exception := task.exception()):
            logger.error(exception)

    async for object_ in iterable:
        if len(tasks) >= max_concurrent_tasks:
            _, tasks = await wait(tasks, return_when=FIRST_COMPLETED)

        task = create_task(function(object_))
        task.add_done_callback(_log_on_exception)

        tasks.add(task)

    await wait(tasks)
