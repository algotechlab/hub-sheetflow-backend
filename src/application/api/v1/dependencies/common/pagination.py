from typing import Annotated

from fastapi import Depends
from src.application.api.v1.schemas.common.pagination import PaginationParamsBaseSchema
from src.core.domain.dtos.common.pagination import PaginationParamsDTO


def get_pagination_params(
    schema: PaginationParamsBaseSchema = Depends(),
) -> PaginationParamsDTO:
    return PaginationParamsDTO(
        filter_by=schema.filter_by,
        filter_value=schema.filter_value,
    )


PaginationParamsDep = Annotated[
    PaginationParamsBaseSchema, Depends(get_pagination_params)
]
