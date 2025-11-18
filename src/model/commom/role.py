import enum


class Role(enum.Enum):
    """Define as permissões de usuário."""

    admin = "admin"
    collaborator = "collaborator"
