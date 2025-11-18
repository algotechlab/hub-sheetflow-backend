import pytest
from sqlalchemy.exc import IntegrityError

from src.model.commons.fields import FieldType
from src.model.groups import Client, ClientGroupData, Group, Mapping


def test_create_group(session):
    group = Group(name="Personal Info", description="Dados pessoais")
    session.add(group)
    session.commit()

    assert group.id is not None
    assert group.name == "Personal Info"
    assert group.is_active is True


def test_group_unique_name(session):
    group1 = Group(name="Financeiro")
    session.add(group1)
    session.commit()

    with pytest.raises(IntegrityError):
        group2 = Group(name="Financeiro")
        session.add(group2)
        session.commit()


def test_create_mapping(session):
    group = Group(name="Endereço")
    session.add(group)
    session.commit()

    mapping = Mapping(
        group_id=group.id,
        name="CEP",
        field_type=FieldType.STRING,
        is_required=True,
        order=1,
    )
    session.add(mapping)
    session.commit()

    assert mapping.id is not None
    assert mapping.group_id == group.id
    assert mapping.field_type == FieldType.STRING


def test_group_relationship_mappings(session):
    group = Group(name="Contato")
    session.add(group)
    session.commit()

    m1 = Mapping(
        group_id=group.id, name="Telefone", field_type=FieldType.STRING
    )
    m2 = Mapping(
        group_id=group.id, name="WhatsApp", field_type=FieldType.STRING
    )

    session.add_all([m1, m2])
    session.commit()

    session.refresh(group)

    assert len(group.mappings) == 2
    assert {m.name for m in group.mappings} == {"Telefone", "WhatsApp"}


def test_create_client(session):
    client = Client(
        name="Maria", email="maria@test.com", cpf_cnpj="12345678900"
    )
    session.add(client)
    session.commit()

    assert client.id is not None
    assert client.name == "Maria"
    assert client.email == "maria@test.com"


def test_unique_constraint_client_group_mapping(session):
    group = Group(name="Documentos")
    session.add(group)

    mapping = Mapping(
        group=group,
        name="RG",
        field_type=FieldType.STRING,
    )
    session.add(mapping)

    client = Client(name="João")
    session.add(client)
    session.commit()

    # Primeiro insert OK
    entry = ClientGroupData(
        client_id=client.id,
        group_id=group.id,
        mapping_id=mapping.id,
        value="123456",
    )
    session.add(entry)
    session.commit()

    # Segundo insert igual deve estourar UNIQUE constraint
    with pytest.raises(IntegrityError):
        duplicated = ClientGroupData(
            client_id=client.id,
            group_id=group.id,
            mapping_id=mapping.id,
            value="999999",
        )
        session.add(duplicated)
        session.commit()


def test_client_group_data_relationships(session):
    group = Group(name="Profissional")
    mapping = Mapping(
        name="Cargo",
        field_type=FieldType.STRING,
        group=group,
    )
    client = Client(name="Carlos")

    session.add_all([group, mapping, client])
    session.commit()

    entry = ClientGroupData(
        client=client,
        group=group,
        mapping=mapping,
        value="Engenheiro",
    )
    session.add(entry)
    session.commit()

    assert entry.id is not None
    assert entry.client.name == "Carlos"
    assert entry.group.name == "Profissional"
    assert entry.mapping.name == "Cargo"
    assert entry.value == "Engenheiro"
