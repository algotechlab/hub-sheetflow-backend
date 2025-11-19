from src.resource import all_namespaces
from src.resource.user import user_us


def test_all_namespaces_includes_user_namespace():
    """A função all_namespaces deve incluir o namespace de usuários."""
    result = all_namespaces()
    assert user_us in result
