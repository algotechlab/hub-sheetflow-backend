from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class Groups(BaseModel):
    name: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )
