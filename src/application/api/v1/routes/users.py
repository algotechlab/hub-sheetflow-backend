from fastapi import APIRouter, status
from src.application.api.v1.dependencies.users import UsersRepositoryDep
from src.application.api.v1.schemas.users import UserBaseSchema, UserOutSchema

tags_metadata = {
    'name': 'Usuários',
    'description': ('Modulo de usuários.'),
}


router = APIRouter(
    prefix='/users',
    tags=[tags_metadata['name']],
)


@router.post(
    '',
    description='Rota para adicionar usuário',
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutSchema,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Usuário criado com sucesso',
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Usuário com email duplicado',
        },
    },
)
async def add_users(
    controller: UsersRepositoryDep,
    users: UserBaseSchema,
) -> UserOutSchema:
    return await controller.add_users(users)
