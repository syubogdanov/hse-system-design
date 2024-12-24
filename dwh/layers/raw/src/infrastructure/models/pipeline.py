from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String

from src.infrastructure.models.base import BaseModel
from src.infrastructure.models.order import OrderModel


class PipelineModel(BaseModel):
    """Модель пайплайна."""

    __tablename__ = "pipeline"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey(OrderModel.id, ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(15))
    message: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
