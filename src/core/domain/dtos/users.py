from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBaseDto(BaseModel):
    """
    Class de entrada para o usuário
    """

    username: str
    email: EmailStr
    password: str


class UserOutDto(BaseModel):
    """
    Class de saída para o usuário
    """

    id: UUID
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
