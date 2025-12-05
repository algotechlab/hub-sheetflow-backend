from typing import List
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import (
    UserEmailDuplicatedException,
    UserNotFoundException,
)
from src.core.domain.service.users import UsersService
from src.core.domain.utils.get_argon import hash_password


class UsersUseCase:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    async def add_users(self, users: UserBaseDto) -> UserOutDto:
        try:
            users.password = hash_password(users.password)
            return await self.users_service.add_users(users)
        except UserEmailDuplicatedException:
            raise UserEmailDuplicatedException(
                f'Esse {users.username} já está cadastrado com {users.email}.'
            )

    async def list_users(self, pagination: PaginationParamsDTO) -> List[UserOutDto]:
        return await self.users_service.list_users(pagination)

    async def update_user(self, user_id: UUID, users: UpdateUserDto) -> UserOutDto:
        result = await self.users_service.update_user(user_id, users)
        if result is None:
            raise UserNotFoundException(f'Esse {user_id} não foi encontrado.')
        return result

    async def delete_user(self, user_id: UUID) -> None:
        result = await self.users_service.delete_user(user_id)

        if result is None:
            raise UserNotFoundException(f'Esse {user_id} não foi encontrado.')
