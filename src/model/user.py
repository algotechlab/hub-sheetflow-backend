from sqlalchemy import Column, Enum as SAEnum, String

from src.model.base import BaseModels
from src.model.commom.role import Role


# Tarefa 1: Definir modelo SQLAlchemy User
class User(BaseModels):
    """
    Modelo da tabela de usuários para autenticação e permissões.
    """

    __tablename__ = "users"

    name = Column(String(100), nullable=False)

    # Tarefa 3: Criar índice único em email
    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    # Vincula o Enum do Python ao banco de dados
    role = Column(SAEnum(Role), nullable=False, default=Role.collaborator)
