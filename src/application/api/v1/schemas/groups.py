from datetime import date, datetime
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
    total_users: int
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class GroupsUpdateSchema(BaseModel):
    name: str


class GroupsMappinsgSchema(BaseModel):
    name: Optional[str] = None
    contato: Optional[str] = None
    documento: Optional[str] = None
    localidade: Optional[str] = None
    numero_processo: Optional[str] = None
    pasta_drive: Optional[bool] = False
    origem: Optional[str] = None
    senha: Optional[str] = None
    orgao_julgador: Optional[str] = None
    contra_parte: Optional[str] = None
    a_ser_feito: Optional[str] = None
    andamento: Optional[str] = None
    observacao: Optional[str] = None
    prazo: Optional[date] = None


class GroupsMappingsUpdateSchema(GroupsMappinsgSchema):
    user_id: UUID


class GroupsMappingsOutSchema(GroupsMappinsgSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class GroupsMappingsListOutSchema(GroupsMappinsgSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
