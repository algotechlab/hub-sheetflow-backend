import json

import pytest

from src.utils.metadata import JsonSerializer, ModelSerializer


def test_model_serializer_to_dict_row(mock_row):
    serializer = ModelSerializer(mock_row)
    result = serializer.to_dict()
    assert isinstance(result, dict)
    assert result.get("id") == 1
    assert result.get("name") == "João"
    assert result.get("email") == "joao@email.com"


def test_model_serializer_to_dict_tuple():
    sample_tuple = (1, "João Silva", "joao@email.com")
    serializer = ModelSerializer(sample_tuple)
    result = serializer.to_dict()
    assert isinstance(result, dict)
    assert result == {
        "col_0": 1,
        "col_1": "João Silva",
        "col_2": "joao@email.com",
    }


def test_model_serializer_to_dict_model(sample_client):
    serializer = ModelSerializer(sample_client)
    result = serializer.to_dict()
    assert isinstance(result, dict)
    assert result["name"] == "João Silva"
    assert result["email"] == "joao@email.com"
    assert result["cpf_cnpj"] == "123.456.789-00"


def test_model_serializer_to_dict_invalid_object():
    serializer = ModelSerializer("invalid_string")
    with pytest.raises(
        ValueError, match="Unable to serialize object: invalid_string"
    ):
        serializer.to_dict()


def test_model_serializer_to_list_single(sample_client):
    serializer = ModelSerializer(sample_client)
    result = serializer.to_list()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "João Silva"


def test_model_serializer_to_list_multiple(sample_clients):
    serializer = ModelSerializer(sample_clients)
    result = serializer.to_list()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "João Silva"
    assert result[1]["name"] == "Maria Santos"


def test_model_serializer_to_list_empty():
    serializer = ModelSerializer([])
    result = serializer.to_list()
    assert isinstance(result, list)
    assert len(result) == 0


def test_model_serializer_to_dict_with_id_model(sample_client):
    serializer = ModelSerializer(sample_client)
    result = serializer.to_dict_with_id()
    assert isinstance(result, dict)
    assert "id" in result  # Assuming id is a column
    assert "name" in result


def test_json_serializer_to_json_dict():
    sample_dict = {"key": "value"}
    serializer = JsonSerializer(sample_dict)
    result = serializer.to_json()
    assert isinstance(result, str)
    assert json.loads(result) == sample_dict


def test_json_serializer_to_json_list():
    sample_list = [{"key": "value1"}, {"key": "value2"}]
    serializer = JsonSerializer(sample_list)
    result = serializer.to_json(as_list=True)
    assert isinstance(result, str)
    assert json.loads(result) == sample_list


def test_json_serializer_to_json_model_single(sample_client):
    serializer = JsonSerializer(sample_client)
    result = serializer.to_json()
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert parsed["name"] == "João Silva"


def test_json_serializer_to_json_model_as_list(sample_client):
    serializer = JsonSerializer(sample_client)
    result = serializer.to_json(as_list=True)
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 1
    assert parsed[0]["name"] == "João Silva"


def test_json_serializer_to_json_model_multiple(sample_clients):
    serializer = JsonSerializer(sample_clients)
    result = serializer.to_json()
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 2


def test_json_serializer_to_json_with_id_model(sample_client):
    serializer = JsonSerializer(sample_client)
    result = serializer.to_json_with_id()
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert "id" in parsed  # Assuming id column


def test_json_serializer_to_json_with_id_no_serializer():
    serializer = JsonSerializer({"key": "value"})
    with pytest.raises(ValueError, match="No ModelSerializer available"):
        serializer.to_json_with_id()
