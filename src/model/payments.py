from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.base import BaseModels


class Payment(BaseModels):
    __tablename__ = "payments"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(
        Float(precision=10, asdecimal=True), nullable=False
    )
    paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
