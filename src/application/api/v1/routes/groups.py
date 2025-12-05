from fastapi import APIRouter, status
from src.application.api.v1.dependencies.groups import GroupsRepositoryDep
from src.application.api.v1.schemas.groups import GroupBaseSchema, GroupOutSchema

tags_metadata = {
    'name': 'Groups',
    'description': ('Modulo de groups.'),
}


router = APIRouter(
    prefix='/groups',
    tags=[tags_metadata['name']],
)


@router.post(
    '',
    description='Rota para adicionar grupo',
    status_code=status.HTTP_201_CREATED,
    response_model=GroupOutSchema,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Grupos criado com sucesso',
        }
    },
)
async def add_groups(
    controller: GroupsRepositoryDep, groups: GroupBaseSchema
) -> GroupOutSchema:
    return await controller.add_groups(groups)
