from src.core.domain.dtos.users import UserBaseDto, UserOutDto
from src.core.domain.interface.users import UsersRepositoriesInterface


class UsersService:
    def __init__(self, users_repository: UsersRepositoriesInterface):
        self.users_repository = users_repository

    async def add_users(self, users: UserBaseDto) -> UserOutDto:
        return await self.users_repository.add_users(users)
