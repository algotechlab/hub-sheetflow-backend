from src.resource.commons.pagination import PaginationArguments


def test_pagination_arguments_defaults():
    instance = PaginationArguments()
    assert instance.current_page == 1
    assert instance.rows_per_page == 10
    assert instance.order_by == ""
    assert instance.sort_by == ""
    assert instance.filter_by == ""


def test_pagination_arguments_with_kwargs():
    instance = PaginationArguments(
        current_page=2,
        rows_per_page=20,
        order_by="name",
        sort_by="asc",
        filter_by="active",
    )
    assert instance.current_page == 2
    assert instance.rows_per_page == 20
    assert instance.order_by == "name"
    assert instance.sort_by == "asc"
    assert instance.filter_by == "active"
