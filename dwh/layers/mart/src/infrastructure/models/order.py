from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.types import DateTime

from src.infrastructure.models.base import BaseModel


class OrderModel(BaseModel):
    """Модель заказа."""

    __tablename__ = "order"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    cost: Mapped[float]
    distance: Mapped[float]
    duration: Mapped[float]
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))