from typing import List
from uuid import UUID

from fastapi import APIRouter, status
from src.application.api.v1.dependencies.common.pagination import PaginationParamsDep
from src.application.api.v1.dependencies.finance import FinanceRepositoryDep
from src.application.api.v1.schemas.finance import (
    FinanceBaseSchema,
    FinanceListInSchema,
    FinanceOutByIdSchema,
    FinanceOutFlowBaseSchema,
    FinanceOutFlowOutSchema,
    FinanceOutSchema,
    HistoryFinanceSchema,
    UpdatedFinanceInstallNumbersOutSchema,
    UpdatedFinanceInstallNumbersSchema,
    UpdatedFinanceOutFlowOutSchema,
    UpdatedFinanceOutFlowSchema,
    UpdateFinanceBaseSchema,
)

tags_metadata = {
    'name': 'Financeiro',
    'description': ('Modulo do financeiro.'),
}


router = APIRouter(
    prefix='/finance',
    tags=[tags_metadata['name']],
)


@router.get(
    '/outflow',
    description='Rota para adicionar a saída de pagamento',
    status_code=status.HTTP_200_OK,
    response_model=List[FinanceOutFlowOutSchema],
    responses={
        status.HTTP_200_OK: {
            'description': 'Desconto listado com sucesso',
        }
    },
)
async def list_finance_out_flow(
    controller: FinanceRepositoryDep, pagination: PaginationParamsDep
) -> List[FinanceOutFlowOutSchema]:
    return await controller.list_finance_out_flow(pagination)


@router.get(
    '/outflow/{outflow_id}',
    description='Rota para detalhar a saída de pagamento',
    status_code=status.HTTP_200_OK,
    response_model=FinanceOutFlowOutSchema,
    responses={
        status.HTTP_200_OK: {
            'description': 'Detalhamento de saida do pagamento',
        }
    },
)
async def get_finance_out_flow(
    controller: FinanceRepositoryDep, outflow_id: UUID
) -> FinanceOutFlowOutSchema:
    return await controller.get_finance_out_flow(outflow_id)


@router.patch(
    '/outflow/{outflow_id}',
    description='Rota para detalhar a saída de pagamento',
    status_code=status.HTTP_200_OK,
    response_model=UpdatedFinanceOutFlowOutSchema,
    responses={
        status.HTTP_200_OK: {
            'description': 'Detalhamento de saida do pagamento',
        }
    },
)
async def updated_finance_out_flow(
    controller: FinanceRepositoryDep,
    outflow_id: UUID,
    outflow: UpdatedFinanceOutFlowSchema,
) -> UpdatedFinanceOutFlowOutSchema:
    return await controller.updated_finance_out_flow(outflow_id, outflow)


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
    '/{finance_id}',
    description='Rota para buscar o pagamento',
    status_code=status.HTTP_200_OK,
    response_model=FinanceOutByIdSchema,
)
async def get_finance(
    controller: FinanceRepositoryDep, finance_id: UUID
) -> FinanceOutByIdSchema:
    return await controller.get_finance(finance_id)


@router.get(
    '/history/{finance_id}',
    description='Rota para buscar o histórico de um pagamento',
    status_code=status.HTTP_200_OK,
    response_model=HistoryFinanceSchema,
)
async def get_history_finance(
    controller: FinanceRepositoryDep, finance_id: UUID
) -> HistoryFinanceSchema:
    return await controller.get_history_finance(finance_id)


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


@router.patch(
    '/{finance_id}',
    description='Rota para atualizar o pagamento',
    status_code=status.HTTP_200_OK,
    response_model=FinanceOutSchema,
)
async def updated_finance(
    controller: FinanceRepositoryDep,
    finance_id: UUID,
    finance: UpdateFinanceBaseSchema,
) -> FinanceOutSchema:
    return await controller.update_finance(finance_id, finance)


@router.patch(
    '/{finance_id}/installments',
    description='Rota para atualizar o pagamento',
    status_code=status.HTTP_200_OK,
    response_model=UpdatedFinanceInstallNumbersOutSchema,
)
async def updated_finance_install_numbers(
    controller: FinanceRepositoryDep,
    finance_id: UUID,
    finance: UpdatedFinanceInstallNumbersSchema,
) -> UpdatedFinanceInstallNumbersOutSchema:
    return await controller.updated_finance_install_numbers(finance_id, finance)


@router.delete(
    '/{finance_id}',
    description='Rota para deletar um pagamento',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_finance(controller: FinanceRepositoryDep, finance_id: UUID):
    return await controller.delete_finance(finance_id)
