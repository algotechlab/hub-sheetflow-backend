from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.model.base import BaseModels


class TestModel(BaseModels):
    __tablename__ = "test_model"
    name: Mapped[str] = mapped_column(nullable=False)


def test_create_model(session):
    item = TestModel(name="Example")
    session.add(item)
    session.commit()
    session.refresh(item)

    # Testa campos obrigatórios
    assert item.id is not None
    assert item.name == "Example"

    # created_at deve ser definido automaticamente
    assert item.created_at is not None
    assert isinstance(item.created_at, datetime)

    # updated_at começa como None
    assert item.updated_at is None

    # Soft delete padrões
    assert item.is_deleted is False
    assert item.deleted_at is None
    assert item.deleted_by is None


def test_soft_delete(session):
    item = TestModel(name="ToDelete")
    session.add(item)
    session.commit()
    session.refresh(item)

    # Marca como deletado
    item.is_deleted = True
    item.deleted_by = 999
    item.deleted_at = datetime.utcnow()

    session.commit()
    session.refresh(item)

    assert item.is_deleted is True
    assert item.deleted_by == 999
    assert isinstance(item.deleted_at, datetime)
