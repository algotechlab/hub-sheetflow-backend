from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.model.base import BaseModels
from src.model.commons.fields import FieldType


class Group(BaseModels):
    """Tabela para definir grupos/abas de campos dinâmicos."""

    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamentos
    mappings: Mapped[list["Mapping"]] = relationship(
        "Mapping", back_populates="group", cascade="all, delete-orphan"
    )
    client_data: Mapped[list["ClientGroupData"]] = relationship(
        "ClientGroupData", back_populates="group", cascade="all, delete-orphan"
    )


class Mapping(BaseModels):
    """Tabela para definir os campos dinâmicos dentro de um grupo."""

    __tablename__ = "mappings"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    field_type: Mapped[str] = mapped_column(SQLEnum(FieldType), nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, default=0)

    group: Mapped["Group"] = relationship("Group", back_populates="mappings")
    client_data_entries: Mapped[list["ClientGroupData"]] = relationship(
        "ClientGroupData", back_populates="mapping"
    )


class Client(BaseModels):
    """Tabela para definir os clientes."""

    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True)
    cpf_cnpj: Mapped[Optional[str]] = mapped_column(String(20))

    # Relacionamentos
    group_data: Mapped[list["ClientGroupData"]] = relationship(
        "ClientGroupData", back_populates="client"
    )


class ClientGroupData(BaseModels):
    __tablename__ = "client_group_data"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), nullable=False, index=True
    )
    mapping_id: Mapped[int] = mapped_column(
        ForeignKey("mappings.id"), nullable=False, index=True
    )
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relacionamentos
    client: Mapped["Client"] = relationship(
        "Client", back_populates="group_data"
    )
    group: Mapped["Group"] = relationship(
        "Group", back_populates="client_data"
    )
    mapping: Mapped["Mapping"] = relationship(
        "Mapping", back_populates="client_data_entries"
    )

    __table_args__ = (UniqueConstraint("client_id", "group_id", "mapping_id"),)
