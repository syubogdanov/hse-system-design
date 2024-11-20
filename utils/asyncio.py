from asyncio import FIRST_COMPLETED, Task, create_task, wait
from collections.abc import AsyncIterator, Callable, Coroutine
from typing import Any, TypeVar


T = TypeVar("T")
R = TypeVar("R")


async def waitmap(
    function: Callable[[T], Coroutine[Any, Any, R]],
    iterable: AsyncIterator[T],
    max_concurrent_tasks: int = 1,
) -> None:
    """Применить функцию ко всем объектам итератора.

    Примечания:
        * Исключения не отменяют выполнение корутин.
    """
    tasks: set[Task] = set()

    async for object_ in iterable:
        if len(tasks) >= max_concurrent_tasks:
            _, tasks = await wait(tasks, return_when=FIRST_COMPLETED)

        task = create_task(function(object_))
        tasks.add(task)

    await wait(tasks)
