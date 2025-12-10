from typing import List
from uuid import UUID

from src.application.api.v1.schemas.groups import (
    GroupsMappingsOutSchema,
    GroupsMappinsgSchema,
)
from src.core.domain.dtos.groups import (
    GroupBaseDto,
    GroupOutDto,
    GroupsListOutDto,
    GroupsUpdateDto,
)
from src.core.domain.exceptions.groups import GroupNotFoundException
from src.core.domain.service.groups import GroupsService


class GroupsUseCase:
    def __init__(self, groups_service: GroupsService):
        self.groups_service = groups_service

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        return await self.groups_service.add_groups(groups)

    async def list_groups(self) -> List[GroupsListOutDto]:
        return await self.groups_service.list_groups()

    async def update_group(self, group_id: UUID, group: GroupsUpdateDto) -> GroupOutDto:
        result = await self.groups_service.update_group(group_id, group)
        if result is None:
            raise GroupNotFoundException(f'Esse {group_id} não foi encontrado.')
        return result

    async def delete_group(self, group_id: UUID) -> None:
        result = await self.groups_service.delete_group(group_id)

        if result is None:
            raise GroupNotFoundException(f'Esse {group_id} não foi encontrado.')

    async def add_user_to_group(
        self, group_id: UUID, mappings: GroupsMappinsgSchema
    ) -> GroupsMappingsOutSchema:
        return await self.groups_service.add_user_to_group(group_id, mappings)

    async def updated_user_to_group(
        self, group_id: UUID, mappings: GroupsMappinsgSchema
    ) -> GroupsMappingsOutSchema:
        return await self.groups_service.updated_user_to_group(group_id, mappings)

    async def delete_user_to_group(self, group_id: UUID, user_id: UUID) -> None:
        return await self.groups_service.delete_user_to_group(group_id, user_id)
