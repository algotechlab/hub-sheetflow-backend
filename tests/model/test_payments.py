from datetime import date, datetime
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.model.groups import Client
from src.model.payments import Payment


def test_client_creation(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Test basic creation with all required fields
    client = Client(
        name="João Silva",
        email="joao@email.com",
        cpf_cnpj="123.456.789-00",
    )
    session.add(client)
    session.commit()

    assert client.id is not None
    assert client.name == "João Silva"
    assert client.email == "joao@email.com"
    assert client.cpf_cnpj == "123.456.789-00"
    assert isinstance(
        client.created_at, datetime
    )  # Assuming BaseModels handles this


def test_client_required_fields(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Test nullable=False fields raise IntegrityError
    # Apenas 'name' é obrigatório (nullable=False)

    # Missing name
    with pytest.raises(IntegrityError):
        invalid_client = Client(
            email="joao@email.com", cpf_cnpj="123.456.789-00"
        )
        session.add(invalid_client)
        session.commit()
    session.rollback()


def test_client_defaults_and_optional(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Campos opcionais: email e cpf_cnpj podem ser None
    client = Client(
        name="João Silva",
        # Sem email ou cpf_cnpj
    )
    session.add(client)
    session.commit()

    assert client.email is None  # Optional field
    assert client.cpf_cnpj is None  # Optional field


def test_client_unique_email(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Test unique constraint on email
    # First insertion
    client1 = Client(
        name="João", email="joao@email.com", cpf_cnpj="123.456.789-00"
    )
    session.add(client1)
    session.commit()

    # Duplicate email
    with pytest.raises(IntegrityError):
        client2 = Client(
            name="Maria",
            email="joao@email.com",  # Duplicate
            cpf_cnpj="987.654.321-00",
        )
        session.add(client2)
        session.commit()
    session.rollback()


def test_payment_creation(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Test basic creation with all required fields
    # Cria Client sem Group (não necessário agora)
    client = Client(
        name="João Silva",
        email="joao@email.com",
        cpf_cnpj="123.456.789-00",
    )
    session.add(client)
    session.commit()

    payment = Payment(
        client_id=client.id,
        due_date=date(2025, 12, 31),
        amount=Decimal("1000.50"),
        paid=False,
    )
    session.add(payment)
    session.commit()

    assert payment.id is not None
    assert payment.client_id == client.id
    assert payment.due_date == date(2025, 12, 31)
    assert payment.amount == Decimal("1000.50")
    assert payment.paid is False
    assert isinstance(
        payment.created_at, datetime
    )  # Assuming BaseModels handles this


def test_payment_required_fields(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    session.execute(text("PRAGMA foreign_keys = ON"))

    # Cria Client básico
    client = Client(
        name="João Silva",
        email="joao@email.com",
        cpf_cnpj="123.456.789-00",
    )
    session.add(client)
    session.commit()

    # Missing due_date
    with pytest.raises(IntegrityError):
        invalid_payment = Payment(
            client_id=client.id, amount=Decimal("1000.50")
        )
        session.add(invalid_payment)
        session.commit()
    session.rollback()

    # Missing amount
    with pytest.raises(IntegrityError):
        invalid_payment = Payment(
            client_id=client.id, due_date=date(2025, 12, 31)
        )
        session.add(invalid_payment)
        session.commit()
    session.rollback()

    # Invalid FK client_id
    with pytest.raises(IntegrityError):
        invalid_payment = Payment(
            client_id=999,
            due_date=date(2025, 12, 31),
            amount=Decimal("1000.50"),
        )
        session.add(invalid_payment)
        session.commit()
    session.rollback()


def test_payment_defaults(session):
    # Clean up tables before test
    session.execute(text("DELETE FROM payments"))
    session.execute(text("DELETE FROM clients"))
    session.commit()

    # Cria Client básico
    client = Client(
        name="João Silva",
        email="joao@email.com",
        cpf_cnpj="123.456.789-00",
    )
    session.add(client)
    session.commit()

    payment = Payment(
        client_id=client.id,
        due_date=date(2025, 12, 31),
        amount=Decimal("1000.50"),
        # paid defaults to False
    )
    session.add(payment)
    session.commit()

    assert payment.paid is False  # Default value
