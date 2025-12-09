from typing import List
from uuid import UUID

from fastapi import APIRouter, status
from src.application.api.v1.dependencies.groups import GroupsRepositoryDep
from src.application.api.v1.schemas.groups import (
    GroupBaseSchema,
    GroupOutSchema,
    GroupsListOutSchema,
    GroupsMappingsOutSchema,
    GroupsMappinsgSchema,
    GroupsUpdateSchema,
)

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


@router.get(
    '',
    description='Rota para listar os grupos',
    status_code=status.HTTP_200_OK,
    response_model=List[GroupsListOutSchema],
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Grupos listado com sucesso',
        }
    },
)
async def list_groups(controller: GroupsRepositoryDep) -> List[GroupsListOutSchema]:
    return await controller.list_groups()


@router.patch(
    '/{group_id}',
    description='Rota para atualizar o nome do grupo',
    status_code=status.HTTP_200_OK,
    response_model=GroupOutSchema,
    responses={
        status.HTTP_200_OK: {
            'description': 'Grupo atualizado com sucesso',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Grupo nao encontrado',
        },
    },
)
async def update_groups(
    controller: GroupsRepositoryDep, group_id: UUID, group: GroupsUpdateSchema
) -> GroupOutSchema:
    return await controller.update_group(group_id, group)


@router.delete(
    '/{group_id}',
    description='Rota para deletar o grupo',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_groups(controller: GroupsRepositoryDep, group_id: UUID) -> None:
    return await controller.delete_group(group_id)


@router.post(
    '/{group_id}/users',
    description='Rota para adicionar um usuário ao grupo',
    status_code=status.HTTP_201_CREATED,
    response_model=GroupsMappingsOutSchema,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Usuário adicionado ao grupo com sucesso',
        },
    },
)
async def add_user_to_group(
    controller: GroupsRepositoryDep, group_id: UUID, mappings: GroupsMappinsgSchema
) -> GroupsMappingsOutSchema:
    return await controller.add_user_to_group(group_id, mappings)


@router.patch(
    '/{group_id}/users',
    description='Rota para atualizar o usuário do grupo',
    status_code=status.HTTP_200_OK,
    response_model=List[GroupsMappingsOutSchema],
    responses={
        status.HTTP_200_OK: {
            'description': 'Tabela de mapeamento atualizada com sucesso',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Grupo nao encontrado',
        },
    },
)
async def updated_user_to_group(
    controller: GroupsRepositoryDep, group_id: UUID, mappings: GroupsMappinsgSchema
) -> GroupsMappingsOutSchema:
    return await controller.updated_user_to_group(group_id, mappings)
