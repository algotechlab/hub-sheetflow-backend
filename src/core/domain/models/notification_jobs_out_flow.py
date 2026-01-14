from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class NotificationJobsOutFlow(BaseModel):
    type: Mapped[str]
    name: Mapped[str]
    date_flow: Mapped[date]
    value: Mapped[Decimal]
    installment_numbers: Mapped[int]
    finance_out_flow_box_id: Mapped[UUID]
    executed: Mapped[bool] = mapped_column(default=False)
