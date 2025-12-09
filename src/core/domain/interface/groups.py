from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.core.domain.dtos.groups import (
    GroupBaseDto,
    GroupOutDto,
    GroupsListOutDto,
    GroupsUpdateDto,
)


class GroupsRepositoriesInterface(ABC):
    @abstractmethod
    async def add_groups(self, groups: GroupBaseDto) -> GroupOutDto: ...

    @abstractmethod
    async def list_groups(self) -> List[GroupsListOutDto]: ...

    @abstractmethod
    async def update_group(
        self, group_id: UUID, group: GroupsUpdateDto
    ) -> GroupOutDto: ...

    @abstractmethod
    async def delete_group(self, group_id: UUID) -> bool: ...
