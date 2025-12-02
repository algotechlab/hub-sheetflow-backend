from fastapi import APIRouter, status
# from src.application.api.v1.dependencies.common.pagination import PaginationParamsDep
# from src.application.api.v1.dependencies.orders import OrdersRepositoryDep
# from src.application.api.v1.schemas.common.exceptions import ExceptionSchema
# from src.application.api.v1.schemas.orders import (
#     OrdersPaginatedOutSchema,
# )

tags_metadata = {
    'name': 'Usuários',
    'description': ('Modulo de usuários.'),
}


router = APIRouter(
    prefix='/users',
    tags=[tags_metadata['name']],
)


# @router.get(
#     '',
#     description='Listagem de pedidos (visualização de matricula).',
#     status_code=status.HTTP_200_OK,
#     response_model=OrdersPaginatedOutSchema,
#     responses={
#         status.HTTP_422_UNPROCESSABLE_ENTITY: {
#             'description': 'Filtros inválidos ou dados incorretos.',
#             'model': ExceptionSchema,
#         },
#     },
# )
# async def list_orders(
#     controller: OrdersRepositoryDep,
#     pagination: PaginationParamsDep,
# ) -> OrdersPaginatedOutSchema:
#     return await controller.list_orders(pagination)
