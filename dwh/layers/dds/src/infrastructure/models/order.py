from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.sqltypes import DateTime, String

from src.infrastructure.models.base import BaseModel


class OrderModel(BaseModel):
    """Модель заказа."""

    __tablename__ = "order"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    source_address_id: Mapped[UUID]
    target_address_id: Mapped[UUID]
    performer_id: Mapped[UUID]
    cost: Mapped[float]
    distance: Mapped[float]
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(15))
    message: Mapped[str | None]
    extra: Mapped[str | None]
