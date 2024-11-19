from typing import Never


def unreachable() -> Never:
    """Метка недостижимого кода."""
    detail = "This code must be unreachable"
    raise RuntimeError(detail)
