from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import DateTime

from src.infrastructure.models.base import BaseModel


class ConfigModel(BaseModel):
    """Модель конфига."""

    __tablename__ = "config"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    min_cost: Mapped[float]
    rubles_per_meter: Mapped[float]
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
