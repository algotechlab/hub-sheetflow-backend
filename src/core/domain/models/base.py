import re
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, func, text
from sqlalchemy.orm import as_declarative, declared_attr, Mapped, mapped_column
from sqlalchemy.schema import MetaData

from src.core.config.settings import get_settings

settings = get_settings()


@as_declarative()
class BaseModel:
    metadata = MetaData(schema=settings.POSTGRES_SCHEMA)

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Converte o nome da classe em snake_case.
        Ex:  UserAccount -> user_account
        """
        cls_name = cls.__name__
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', cls_name).lower()
        return snake
