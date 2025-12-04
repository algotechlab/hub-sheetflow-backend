from typing import List

from src.application.api.v1.schemas.common.pagination import PaginationParamsBaseSchema
from src.application.api.v1.schemas.users import UserBaseSchema, UserOutSchema
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UserBaseDto
from src.core.domain.use_case.users import UsersUseCase


class UsersController:
    def __init__(self, use_case: UsersUseCase):
        self.use_case = use_case

    async def add_users(self, users: UserBaseSchema) -> UserOutSchema:
        users_dto = UserBaseDto(**users.model_dump())
        users_case = await self.use_case.add_users(users_dto)
        return UserOutSchema.model_validate(users_case)

    async def list_users(
        self, pagination: PaginationParamsBaseSchema
    ) -> List[UserOutSchema]:
        pagination_dto = PaginationParamsDTO(**pagination.model_dump())
        users = await self.use_case.list_users(pagination_dto)
        return [UserOutSchema.model_validate(user) for user in users]
