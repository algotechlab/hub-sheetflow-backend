from fastapi import APIRouter, status
from src.application.api.v1.dependencies.login import LoginControllerDep
from src.application.api.v1.schemas.login import LoginInSchema, LoginOutSchema

tags_metadata = {
    'name': 'Login',
    'description': ('Modulo de login.'),
}


router = APIRouter(
    prefix='/login',
    tags=[tags_metadata['name']],
)


@router.post(
    '',
    description='Rota para realizar login.',
    status_code=status.HTTP_201_CREATED,
    response_model=LoginOutSchema,
)
async def login(
    login_controller: LoginControllerDep,
    login: LoginInSchema,
) -> str:
    return await login_controller.login(login)
