from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from src.infrastructure.models.base import BaseModel
from src.infrastructure.models.pipeline import PipelineModel


class DeliveryModel(BaseModel):
    """Модель доставки."""

    __tablename__ = "delivery"

    pipeline_id: Mapped[UUID] = mapped_column(
        ForeignKey(PipelineModel.id, ondelete="CASCADE"),
        primary_key=True,
    )

    cost: Mapped[float | None]
    estimated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    performer_id: Mapped[UUID | None]
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
