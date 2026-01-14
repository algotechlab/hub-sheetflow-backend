from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class IndicatorAnalysisBaseDto(BaseModel):
    # Core
    total_groups: Optional[int] = None
    total_users: Optional[int] = None
    total_clients: Optional[int] = None

    # Financeiro
    total_to_receive: Optional[Decimal] = None
    total_exit: Optional[Decimal] = None
    net_balance: Optional[Decimal] = None

    # Parcelas
    total_pending_installments: Optional[int] = None
    total_installments: Optional[int] = None

    # KPIs derivados
    average_ticket: Optional[Decimal] = None
    exit_percentage: Optional[Decimal] = None
    default_rate: Optional[Decimal] = None
    revenue_per_group: Optional[Decimal] = None
