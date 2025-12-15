from typing import List

from fastapi import APIRouter, status
from src.application.api.v1.dependencies.common.pagination import PaginationParamsDep
from src.application.api.v1.dependencies.finance import FinanceRepositoryDep
from src.application.api.v1.schemas.finance import (
    FinanceBaseSchema,
    FinanceListInSchema,
    FinanceOutFlowBaseSchema,
    FinanceOutFlowOutSchema,
    FinanceOutSchema,
)

tags_metadata = {
    'name': 'Financeiro',
    'description': ('Modulo do financeiro.'),
}


router = APIRouter(
    prefix='/finance',
    tags=[tags_metadata['name']],
)


@router.post(
    '',
    description='Rota para adicionar o pagamento',
    status_code=status.HTTP_201_CREATED,
    response_model=FinanceOutSchema,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Pagamento criado com sucesso',
        }
    },
)
async def add_finance(
    controller: FinanceRepositoryDep, finance: FinanceBaseSchema
) -> FinanceOutSchema:
    return await controller.add_finance(finance)


@router.get(
    '',
    description='Rota para listar o pagamento',
    status_code=status.HTTP_201_CREATED,
    response_model=List[FinanceListInSchema],
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Pagamento listado com sucesso',
        }
    },
)
async def list_finance(
    controller: FinanceRepositoryDep, pagination: PaginationParamsDep
) -> List[FinanceListInSchema]:
    return await controller.list_finance(pagination)


@router.post(
    '/outflow',
    description='Rota para adicionar a saída de pagamento',
    status_code=status.HTTP_201_CREATED,
    response_model=FinanceOutFlowOutSchema,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Desconto criado com sucesso',
        }
    },
)
async def add_finance_out_flow(
    controller: FinanceRepositoryDep, outflow: FinanceOutFlowBaseSchema
) -> FinanceOutFlowOutSchema:
    return await controller.add_finance_outflow(outflow)
