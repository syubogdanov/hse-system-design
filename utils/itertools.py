from asyncio import FIRST_COMPLETED, Task, create_task, wait
from collections.abc import AsyncIterable, Callable, Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


async def aiomap(
    func: Callable[[T], Coroutine[Any, Any, None]],
    iterable: AsyncIterable[T],
    max_concurrent_tasks: int = 1,
) -> None:
    """Конкурентно применить функцию."""
    tasks: set[Task] = set()

    async for item in iterable:
        if len(tasks) >= max_concurrent_tasks:
            _, tasks = await wait(tasks, return_when=FIRST_COMPLETED)

        task = create_task(func(item))
        tasks.add(task)

    await wait(tasks)
