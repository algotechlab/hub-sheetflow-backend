from uuid import UUID

from pydantic import BaseModel


class LoginDTO(BaseModel):
    email: str
    password: str


class LoginResponseDTO(LoginDTO):
    username: str
    user_id: UUID
    token: str
    role: str
