from datetime import date
from decimal import Decimal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class FinanceOutFlowBox(BaseModel):
    value: Mapped[Decimal] = mapped_column(
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    installment_numbers: Mapped[int] = mapped_column(
        nullable=True,
    )
    date_flow: Mapped[date] = mapped_column(
        nullable=True,
    )
