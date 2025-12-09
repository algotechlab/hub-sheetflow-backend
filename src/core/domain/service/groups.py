from typing import List
from uuid import UUID

from src.core.domain.dtos.groups import (
    GroupBaseDto,
    GroupOutDto,
    GroupsListOutDto,
    GroupsUpdateDto,
)
from src.core.domain.interface.groups import GroupsRepositoriesInterface


class GroupsService:
    def __init__(self, groups_repository: GroupsRepositoriesInterface):
        self.groups_repository = groups_repository

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        return await self.groups_repository.add_groups(groups)

    async def list_groups(self) -> List[GroupsListOutDto]:
        return await self.groups_repository.list_groups()

    async def update_group(self, group_id: UUID, group: GroupsUpdateDto) -> GroupOutDto:
        return await self.groups_repository.update_group(group_id, group)

    async def delete_group(self, group_id: UUID) -> bool:
        return await self.groups_repository.delete_group(group_id)
