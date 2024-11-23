import tomllib

from pathlib import Path


def get_version() -> str:
    """Получить версию проекта."""
    with Path("pyproject.toml").open(mode="rb") as file:
        data = tomllib.load(file)
        return data["tool"]["poetry"]["version"]
