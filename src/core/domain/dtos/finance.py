from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
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


class UpdatedFinanceOutFlowDto(BaseModel):
    description: Optional[str] = None
    value: Optional[Decimal] = None
    date_flow: Optional[date] = None
    installment_numbers: Optional[int] = None


class UpdatedFinanceOutFlowOutDto(UpdatedFinanceOutFlowDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class InstallmentOutDto(BaseModel):
    installment_number: int
    paid_at: datetime | None
    due_date: datetime
    value: Decimal
    charged_at: datetime | None

    model_config = {'from_attributes': True}


class FinanceOutByIdDto(BaseModel):
    id: UUID
    name: str
    date_contract: date
    document: str
    total: Decimal
    installments: list[InstallmentOutDto]

    model_config = {'from_attributes': True}


class InstallmentOutFlowDto(BaseModel):
    installment_number: int
    paid_at: datetime | None
    due_date: datetime
    value: Decimal
    charged_at: datetime | None

    model_config = {'from_attributes': True}


class FinanceOutFlowByIdDto(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    description: str
    value: Decimal
    date_flow: date
    installment_numbers: Optional[int] = None
    installments: list[InstallmentOutDto]

    model_config = {'from_attributes': True}


class HistoryFinanceDto(FinanceBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
    installment_value: Decimal
    total_calculated: Decimal
    model_config = {'from_attributes': True}


class InstallmentUpdateItem(BaseModel):
    installment_number: int
    paid_at: Optional[datetime] = None


class UpdatedFinanceInstallNumbersDto(BaseModel):
    installments: List[InstallmentUpdateItem]


class UpdatedFinanceInstallNumbersOutDto(UpdatedFinanceInstallNumbersDto):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UpdatedFinanceOutFlowInstallNumbersDto(BaseModel):
    installments: List[InstallmentUpdateItem]


class UpdatedFinanceOutFlowInstallNumbersOutDto(UpdatedFinanceOutFlowInstallNumbersDto):
    id: UUID
    created_at: datetime
    updated_at: datetime
