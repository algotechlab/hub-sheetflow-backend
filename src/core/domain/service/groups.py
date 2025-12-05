from src.core.domain.dtos.groups import GroupBaseDto, GroupOutDto
from src.core.domain.interface.groups import GroupsRepositoriesInterface


class GroupsService:
    def __init__(self, groups_repository: GroupsRepositoriesInterface):
        self.groups_repository = groups_repository

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        return await self.groups_repository.add_groups(groups)
