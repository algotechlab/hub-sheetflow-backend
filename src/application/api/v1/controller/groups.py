from typing import List
from uuid import UUID

from src.application.api.v1.schemas.common.pagination import PaginationParamsBaseSchema
from src.application.api.v1.schemas.groups import (
    GroupBaseSchema,
    GroupOutSchema,
    GroupsListOutSchema,
    GroupsMappingsListOutSchema,
    GroupsMappingsOutSchema,
    GroupsMappinsgSchema,
    GroupsUpdateSchema,
)
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.groups import GroupBaseDto, GroupsMappingsDto, GroupsUpdateDto
from src.core.domain.use_case.groups import GroupsUseCase


class GroupsController:
    def __init__(self, use_case: GroupsUseCase):
        self.use_case = use_case

    async def add_groups(self, groups: GroupBaseSchema) -> GroupOutSchema:
        groups_dto = GroupBaseDto(**groups.model_dump())
        groups_case = await self.use_case.add_groups(groups_dto)
        return GroupOutSchema.model_validate(groups_case)

    async def list_groups(self) -> GroupsListOutSchema:
        groups_case = await self.use_case.list_groups()
        return [GroupsListOutSchema.model_validate(group) for group in groups_case]

    async def update_group(
        self, group_id: UUID, group: GroupsUpdateSchema
    ) -> GroupOutSchema:
        group_dto = GroupsUpdateDto(**group.model_dump())
        group_case = await self.use_case.update_group(group_id, group_dto)
        return GroupOutSchema.model_validate(group_case)

    async def delete_group(self, group_id: UUID) -> None:
        return await self.use_case.delete_group(group_id)

    async def add_user_to_group(
        self, group_id: UUID, mappings: GroupsMappinsgSchema
    ) -> GroupsMappingsOutSchema:
        mappings_dto = GroupsMappingsDto(**mappings.model_dump())
        mappings_case = await self.use_case.add_user_to_group(group_id, mappings_dto)
        return GroupsMappingsOutSchema.model_validate(mappings_case)

    async def list_users_to_grupo(
        self, pagination: PaginationParamsBaseSchema, group_id: UUID
    ) -> List[GroupsMappingsListOutSchema]:
        pagination_dto = PaginationParamsDTO(**pagination.model_dump())
        groups = await self.use_case.list_users_to_grupo(pagination_dto, group_id)
        return [GroupsMappingsListOutSchema.model_validate(group) for group in groups]

    async def updated_user_to_group(
        self, group_id: UUID, mappings: GroupsMappinsgSchema
    ) -> GroupsMappingsOutSchema:
        mappings_dto = GroupsMappingsDto(**mappings.model_dump())
        mappings_case = await self.use_case.updated_user_to_group(
            group_id, mappings_dto
        )
        return [
            GroupsMappingsOutSchema.model_validate(mapping) for mapping in mappings_case
        ]

    async def delete_user_to_group(self, group_id: UUID, user_id: UUID) -> None:
        return await self.use_case.delete_user_to_group(group_id, user_id)

    async def transfer_user_to_group(self, group_id: UUID, user_id: UUID) -> None:
        return await self.use_case.transfer_user_to_group(group_id, user_id)
