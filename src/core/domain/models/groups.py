from typing import Any, Dict, List

from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class Groups(BaseModel):
    name: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )

    data: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=True,
    )

    custom_columns: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=False,
    )

    __table_args__ = (
        Index('ix_groups_data_gin', data, postgresql_using='gin'),
        Index('ix_groups_custom_columns_gin', custom_columns, postgresql_using='gin'),
    )
