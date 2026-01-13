from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class InstallmentPayment(BaseModel):
    installment_number: Mapped[int] = mapped_column(nullable=False)
    value: Mapped[Decimal] = mapped_column(nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    paid_at: Mapped[datetime] = mapped_column(nullable=True)
    charged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    finance_id: Mapped[UUID] = mapped_column(
        ForeignKey('finance.id'),
        nullable=False,
    )
