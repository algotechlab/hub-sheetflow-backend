from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CustomColumn(BaseModel):
    name: str
    label: str
    type: str


class GroupBaseSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    data: Optional[Dict[str, str]]
    custom_columns: Optional[list[CustomColumn]] = Field(default=None)


class GroupOutSchema(GroupBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
