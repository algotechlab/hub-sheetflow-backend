from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class InstallmentPaymentBaseDto(BaseModel):
    name: str
    value: Decimal
    date_contract: datetime
