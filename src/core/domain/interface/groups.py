from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.groups import (
    GroupBaseDto,
    GroupOutDto,
    GroupsListOutDto,
    GroupsMappingsDto,
    GroupsMappingsOutDto,
    GroupsMappinsgListOutDto,
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

    @abstractmethod
    async def add_user_to_group(
        self, group_id: UUID, mappings: GroupsMappingsDto
    ) -> GroupsMappingsOutDto: ...

    @abstractmethod
    async def list_users_to_grupo(
        self, pagination: PaginationParamsDTO, group_id: UUID
    ) -> List[GroupsMappinsgListOutDto]: ...

    @abstractmethod
    async def updated_user_to_group(
        self, group_id: UUID, mappings: GroupsMappingsDto
    ) -> GroupsMappingsOutDto: ...

    @abstractmethod
    async def delete_user_to_group(self, group_id: UUID, user_id: UUID) -> bool: ...

    @abstractmethod
    async def transfer_user_to_group(self, group_id: UUID, user_id: UUID) -> None: ...
