from datetime import date
from decimal import Decimal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class Finance(BaseModel):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    date_contract: Mapped[date] = mapped_column(
        nullable=False,
    )
    document: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    installment_numbers: Mapped[int] = mapped_column(
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        nullable=False,
    )
