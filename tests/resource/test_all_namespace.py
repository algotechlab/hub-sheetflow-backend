from src.resource import all_namespaces


def test_all_namespaces_returns_empty_list():
    """A função all_namespaces deve retornar lista vazia."""
    result = all_namespaces()
    assert isinstance(result, list)
    assert result == []
