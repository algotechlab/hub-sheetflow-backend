from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FinanceBaseDto(BaseModel):
    name: str
    date_contract: date
    document: str
    installment_numbers: int
    total: Decimal


class UpdateFinanceBaseDto(BaseModel):
    name: Optional[str] = None
    date_contract: Optional[date] = None
    document: Optional[str] = None
    installment_numbers: Optional[int] = None
    total: Optional[Decimal] = None


class FinanceOutDto(FinanceBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceListOutDto(FinanceBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceOutFlowBaseDto(BaseModel):
    description: str
    value: Decimal
    date_flow: date
    installment_numbers: Optional[int] = None


class FinanceOutFlowOutDto(FinanceOutFlowBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceOutByIdDto(FinanceBaseDto):
    id: UUID
    name: str
    date_contract: date
    document: str
    installment_numbers: int
    total: Decimal
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}
