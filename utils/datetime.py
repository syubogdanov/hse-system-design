from datetime import UTC, datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pydantic import AwareDatetime


def utcnow() -> "AwareDatetime":
    """Текущее время по `UTC`."""
    return datetime.now(UTC)
