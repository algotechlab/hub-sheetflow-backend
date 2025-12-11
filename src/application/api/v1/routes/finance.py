from fastapi import APIRouter, status
from src.application.api.v1.dependencies.finance import FinanceRepositoryDep
from src.application.api.v1.schemas.finance import FinanceBaseSchema, FinanceOutSchema

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
