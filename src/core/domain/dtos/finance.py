from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class FinanceBaseDto(BaseModel):
    name: str
    date_contract: date
    document: str
    installment_numbers: int
    total: Decimal


class FinanceOutDto(FinanceBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}
