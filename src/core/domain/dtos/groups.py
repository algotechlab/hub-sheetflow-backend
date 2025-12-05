from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GroupBaseDto(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    data: Optional[Dict[str, str]]
    custom_columns: Optional[List[Dict[str, str]]] = None


class GroupOutDto(GroupBaseDto):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
