from datetime import datetime
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


class GrupsUpdateSchema(BaseModel):
    name: str
