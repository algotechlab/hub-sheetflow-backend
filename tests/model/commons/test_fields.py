import pytest

from src.model.commons.fields import FieldType


def test_fieldtype_values():
    """Valida se os valores estão corretos."""
    assert FieldType.STRING.value == "string"
    assert FieldType.INTEGER.value == "integer"
    assert FieldType.FLOAT.value == "float"
    assert FieldType.DATE.value == "date"
    assert FieldType.BOOLEAN.value == "boolean"
    assert FieldType.TEXT.value == "text"


def test_fieldtype_is_enum():
    """Garante que cada item é realmente um Enum."""
    assert isinstance(FieldType.STRING, FieldType)
    assert isinstance(FieldType.INTEGER, FieldType)
    assert isinstance(FieldType.FLOAT, FieldType)


def test_fieldtype_iteration():
    """Enum deve ser iterável e ter todos os membros."""
    expected = {
        "string",
        "integer",
        "float",
        "date",
        "boolean",
        "text",
    }
    values = {ft.value for ft in FieldType}
    assert expected == values


def test_fieldtype_from_value():
    """Garante que o Enum pode ser recuperado por valor."""
    assert FieldType("string") is FieldType.STRING
    assert FieldType("integer") is FieldType.INTEGER
    assert FieldType("float") is FieldType.FLOAT
    assert FieldType("date") is FieldType.DATE
    assert FieldType("boolean") is FieldType.BOOLEAN
    assert FieldType("text") is FieldType.TEXT


def test_fieldtype_invalid_value():
    """Busca por valor inválido deve disparar ValueError."""
    with pytest.raises(ValueError):
        FieldType("INVALID")


def test_fieldtype_immutable():
    """Enums devem ser imutáveis."""
    with pytest.raises(AttributeError):
        FieldType.STRING.value = "new_value"
