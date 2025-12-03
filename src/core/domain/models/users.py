from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.config.settings import get_settings
from src.core.domain.models.base import BaseModel

settings = get_settings()


class User(BaseModel):
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
