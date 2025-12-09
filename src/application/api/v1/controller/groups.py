from uuid import UUID

from src.application.api.v1.schemas.groups import (
    GroupBaseSchema,
    GroupOutSchema,
    GroupsListOutSchema,
    GrupsUpdateSchema,
)
from src.core.domain.dtos.groups import GroupBaseDto, GroupsUpdateDto
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
        self, group_id: UUID, group: GrupsUpdateSchema
    ) -> GroupOutSchema:
        group_dto = GroupsUpdateDto(**group.model_dump())
        group_case = await self.use_case.update_group(group_id, group_dto)
        return GroupOutSchema.model_validate(group_case)

    async def delete_group(self, group_id: UUID) -> None:
        return await self.use_case.delete_group(group_id)
