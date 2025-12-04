from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBaseSchema(BaseModel):
    """
    Class de entrada para o usuário
    """

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=255)

    @field_validator('username', mode='after')
    def username_must_be_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('username must be alphanumeric')
        return value

    @field_validator('password', mode='after')
    def password_must_be_strong(cls, value: str) -> str:
        value_exp = 8
        if len(value) < value_exp:
            raise ValueError('password must be at least 8 characters long')
        return value


class UserOutSchema(BaseModel):
    """
    Class de saída para o usuário
    """

    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
