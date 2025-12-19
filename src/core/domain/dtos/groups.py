from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GroupBaseDto(BaseModel):
    name: str = Field(min_length=3, max_length=20)


class GroupOutDto(GroupBaseDto):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class GroupsListOutDto(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class GroupsUpdateDto(GroupBaseDto):
    name: str
    model_config = {'from_attributes': True}


class GroupsMappingsDto(BaseModel):
    name: Optional[str] = None
    depedencias_pid: Optional[str] = None
    localidade: Optional[str] = None
    contato: Optional[str] = None
    pasta_drive: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    senha_portal: Optional[str] = None
    aba_plataforma: Optional[str] = None
    status: Optional[str] = None
    data_atual: Optional[date] = None
    data_intimacao: Optional[date] = None
    prazo: Optional[str] = None
    data_final: Optional[date] = None
    oficio: Optional[str] = None
    valor_indenizacao: Optional[Decimal] = None
    valor_honorario: Optional[Decimal] = None
    observacao: Optional[str] = None


class GroupsMappingsOutDto(GroupsMappingsDto):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class GroupsMappinsgListOutDto(GroupsMappingsDto):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
