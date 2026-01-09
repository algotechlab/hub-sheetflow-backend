from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FinanceBaseSchema(BaseModel):
    name: str
    date_contract: date
    document: str
    installment_numbers: int
    total: Decimal


class UpdateFinanceBaseSchema(BaseModel):
    name: Optional[str] = None
    date_contract: Optional[date] = None
    document: Optional[str] = None
    installment_numbers: Optional[int] = None
    total: Optional[Decimal] = None


class FinanceOutSchema(FinanceBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceListInSchema(FinanceBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceOutFlowBaseSchema(BaseModel):
    description: str
    value: Decimal
    date_flow: date
    installment_numbers: Optional[int] = None


class FinanceOutFlowOutSchema(FinanceOutFlowBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class UpdatedFinanceOutFlowSchema(BaseModel):
    description: Optional[str] = None
    value: Optional[Decimal] = None
    date_flow: Optional[date] = None
    installment_numbers: Optional[int] = None


class UpdatedFinanceOutFlowOutSchema(UpdatedFinanceOutFlowSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class FinanceOutByIdSchema(BaseModel):
    id: UUID
    name: str
    date_contract: date
    document: str
    installment_numbers: int
    total: Decimal
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class HistoryFinanceSchema(FinanceBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    installment_value: Decimal
    total_calculated: Decimal
    model_config = {'from_attributes': True}
