from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class MappingsGroups(BaseModel):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    contato: Mapped[str] = mapped_column(String(255), nullable=True)
    documento: Mapped[str] = mapped_column(String(20), nullable=True)
    pasta_drive: Mapped[bool] = mapped_column(Boolean, default=False)
    localidade: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_processo: Mapped[str] = mapped_column(String(255), nullable=True)
    origem: Mapped[str] = mapped_column(String(255), nullable=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=True)
    orgao_julgador: Mapped[str] = mapped_column(String(255), nullable=True)
    contra_parte: Mapped[str] = mapped_column(String(255), nullable=True)
    a_ser_feito: Mapped[str] = mapped_column(nullable=True)
    andamento: Mapped[str] = mapped_column(String(255), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)
    prazo: Mapped[date] = mapped_column(Date, nullable=True)
    groups_id: Mapped[str] = mapped_column(
        ForeignKey('groups.id'),
        nullable=False,
    )
