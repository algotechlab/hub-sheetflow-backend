from datetime import datetime

import pytest

from src.model.commons.role import Role
from src.model.user import User


def test_create_user(session):
    user = User(
        name="Hedris",
        email="hedris@example.com",
        password_hash="hashedpassword",
        role=Role.collaborator,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.name == "Hedris"
    assert user.email == "hedris@example.com"
    assert user.password_hash == "hashedpassword"
    assert user.role == Role.collaborator

    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is None
    assert user.is_deleted is False


def test_user_email_unique_constraint(session):
    user1 = User(
        name="John",
        email="unique@example.com",
        password_hash="abc",
        role=Role.admin,
    )
    session.add(user1)
    session.commit()

    user2 = User(
        name="Doe",
        email="unique@example.com",  # mesmo email → deve falhar
        password_hash="123",
        role=Role.collaborator,
    )

    session.add(user2)

    with pytest.raises(Exception):
        session.commit()  # deve lançar erro por unique constraint

    session.rollback()


def test_update_user(session):
    user = User(
        name="Test",
        email="test@ex.com",
        password_hash="pwd",
        role=Role.collaborator,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # update
    user.name = "Updated"
    session.commit()
    session.refresh(user)

    assert user.name == "Updated"
    assert isinstance(user.created_at, datetime)
    assert hasattr(user, "updated_at")


def test_role_enum(session):
    user = User(
        name="RoleTest",
        email="role@example.com",
        password_hash="pwd",
        role=Role.admin,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.role == Role.admin
