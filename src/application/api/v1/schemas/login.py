from uuid import UUID

from pydantic import BaseModel


class LoginInSchema(BaseModel):
    email: str
    password: str


class LoginOutSchema(LoginInSchema):
    user_id: UUID
    token: str
    role: str
