import tomllib

from utils.basedir import BASEDIR


def get_version() -> str:
    """Получить версию проекта."""
    path = BASEDIR / "pyproject.toml"

    with path.open(mode="rb") as file:
        pyproject = tomllib.load(file)
        return pyproject["tool"]["poetry"]["version"]
