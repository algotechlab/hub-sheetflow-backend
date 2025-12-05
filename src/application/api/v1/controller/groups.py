from src.application.api.v1.schemas.groups import GroupBaseSchema, GroupOutSchema
from src.core.domain.dtos.groups import GroupBaseDto
from src.core.domain.use_case.groups import GroupsUseCase


class GroupsController:
    def __init__(self, use_case: GroupsUseCase):
        self.use_case = use_case

    async def add_groups(self, groups: GroupBaseSchema) -> GroupOutSchema:
        groups_dto = GroupBaseDto(**groups.model_dump())
        groups_case = await self.use_case.add_groups(groups_dto)
        return GroupOutSchema.model_validate(groups_case)
