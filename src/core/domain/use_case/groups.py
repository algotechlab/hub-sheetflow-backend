from src.core.domain.dtos.groups import GroupBaseDto, GroupOutDto
from src.core.domain.service.groups import GroupsService


class GroupsUseCase:
    def __init__(self, groups_service: GroupsService):
        self.groups_service = groups_service

    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto:
        return await self.groups_service.add_groups(groups)
