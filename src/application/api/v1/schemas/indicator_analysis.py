from decimal import Decimal

from pydantic import BaseModel


class IndicatorAnalysisBaseSchema(BaseModel):
    # Core
    total_groups: int
    total_users: int
    total_clients: int

    # Financeiro
    total_to_receive: Decimal
    total_exit: Decimal
    net_balance: Decimal

    # Parcelas
    total_pending_installments: int
    total_installments: int

    # KPIs derivados
    average_ticket: Decimal  # ticket médio
    exit_percentage: Decimal  # % saídas / receitas
    default_rate: Decimal  # % inadimplência
    revenue_per_group: Decimal  # receita média por grupo
