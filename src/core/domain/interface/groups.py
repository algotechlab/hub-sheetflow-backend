from abc import ABC, abstractmethod

from src.core.domain.dtos.groups import GroupBaseDto, GroupOutDto


class GroupsRepositoriesInterface(ABC):
    @abstractmethod
    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto: ...
