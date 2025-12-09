from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.domain.models.base import BaseModel


class MappingsGroups(BaseModel):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    depedencias_pid: Mapped[str] = mapped_column(String(255), nullable=True)
    localidade: Mapped[str] = mapped_column(String(255), nullable=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=True)
    contato: Mapped[str] = mapped_column(String(255), nullable=True)
    pasta_drive: Mapped[str] = mapped_column(String(255), nullable=True)
    cpf_cnpj: Mapped[str] = mapped_column(String(255), nullable=True)
    senha_portal: Mapped[str] = mapped_column(String(255), nullable=True)
    aba_plataforma: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    data_atual: Mapped[str] = mapped_column(String(255), nullable=True)
    data_intimacao: Mapped[str] = mapped_column(String(255), nullable=True)
    prazo: Mapped[str] = mapped_column(String(255), nullable=True)
    data_final: Mapped[str] = mapped_column(String(255), nullable=True)
    oficio: Mapped[str] = mapped_column(String(255), nullable=True)
    valor_indenizacao: Mapped[str] = mapped_column(String(255), nullable=True)
    valor_honorario: Mapped[str] = mapped_column(String(255), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)
    groups_id: Mapped[str] = mapped_column(
        ForeignKey('groups.id'),
        nullable=False,
    )
