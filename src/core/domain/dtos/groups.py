from datetime import datetime
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
