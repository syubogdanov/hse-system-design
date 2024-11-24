from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.session import AsyncSession


SessionFactory = Callable[[], AbstractAsyncContextManager["AsyncSession"]]
