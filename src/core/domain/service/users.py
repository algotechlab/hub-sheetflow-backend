from typing import List, Union
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto
from src.core.domain.interface.users import UsersRepositoriesInterface


class UsersService:
    def __init__(self, users_repository: UsersRepositoriesInterface):
        self.users_repository = users_repository

    async def add_users(self, users: UserBaseDto) -> UserOutDto:
        return await self.users_repository.add_users(users)

    async def list_users(self, pagination: PaginationParamsDTO) -> List[UserOutDto]:
        return await self.users_repository.list_users(pagination)

    async def update_user(
        self, user_id: UUID, users: UpdateUserDto
    ) -> Union[UserOutDto, None]:
        return await self.users_repository.update_user(user_id, users)
