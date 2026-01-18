from datetime import date
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class NotificationCourtDeadline(BaseModel):
    type: Mapped[str]
    name: Mapped[str]
    contato: Mapped[str]
    document: Mapped[str]
    prazo: Mapped[date]
    groups_id: Mapped[UUID]
    mappings_groups_id: Mapped[UUID]
    executed: Mapped[bool] = mapped_column(default=False)
