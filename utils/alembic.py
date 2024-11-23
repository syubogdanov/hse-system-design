from alembic.config import Config

from utils.basedir import BASEDIR


def get_config(url: str) -> Config:
    """Подготовить конфиг для миграций."""
    config = Config(BASEDIR / "migrations" / "alembic.ini")
    config.set_main_option("sqlalchemy.url", url)
    return config
