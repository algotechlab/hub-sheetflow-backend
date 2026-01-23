from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class CourtDeadline(BaseModel):
    name: Mapped[str]
    contato: Mapped[str] = mapped_column(String(255), nullable=True)
    document: Mapped[str] = mapped_column(String(255), nullable=True)
    prazo: Mapped[date] = mapped_column(Date, nullable=True)
    charged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    groups_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'), nullable=False)
    mappings_groups_id: Mapped[UUID] = mapped_column(
        ForeignKey('mappings_groups.id'), nullable=False
    )
