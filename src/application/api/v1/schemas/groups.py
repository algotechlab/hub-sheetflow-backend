from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GroupBaseSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20)


class GroupOutSchema(GroupBaseSchema):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class GroupsListOutSchema(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class GroupsUpdateSchema(BaseModel):
    name: str


class GroupsMappinsgSchema(BaseModel):
    depedencias_pid: Optional[str] = None
    localidade: Optional[str] = None
    name: Optional[str] = None
    contato: Optional[str] = None
    pasta_drive: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    senha_portal: Optional[str] = None
    aba_plataforma: Optional[str] = None
    status: Optional[str] = None
    data_atual: Optional[str] = None
    data_intimacao: Optional[str] = None
    prazo: Optional[str] = None
    data_final: Optional[str] = None
    oficio: Optional[str] = None
    valor_indenizacao: Optional[str] = None
    valor_honorario: Optional[str] = None
    observacao: Optional[str] = None


class GroupsMappingsOutSchema(GroupsMappinsgSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class GroupsMappingsListOutSchema(GroupsMappinsgSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
