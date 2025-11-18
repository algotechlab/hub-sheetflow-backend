from sqlalchemy import Column, Enum as SAEnum, String

from src.model.base import BaseModels
from src.model.commons.role import Role


class User(BaseModels):
    """
    Modelo da tabela de usuários para autenticação e permissões.
    """

    __tablename__ = "users"

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    role = Column(SAEnum(Role), nullable=False, default=Role.collaborator)
