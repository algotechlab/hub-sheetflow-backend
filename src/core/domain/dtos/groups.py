from datetime import datetime
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
    contato: Optional[str] = None
    documento: Optional[str] = None
    localidade: Optional[str] = None
    pasta_drive: Optional[bool] = False
    origem: Optional[str] = None
    senha: Optional[str] = None
    orgao_julgador: Optional[str] = None
    contra_parte: Optional[str] = None
    a_ser_feito: Optional[str] = None
    andamento: Optional[str] = None
    observacao: Optional[str] = None


class GroupsMappingsUpdateDto(GroupsMappingsDto):
    user_id: UUID

    model_config = {'from_attributes': True}


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
