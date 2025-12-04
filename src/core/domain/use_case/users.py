from src.core.domain.dtos.users import UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import UserEmailDuplicatedException
from src.core.domain.service.users import UsersService


class UsersUseCase:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    async def add_users(self, users: UserBaseDto) -> UserOutDto:
        try:
            return await self.users_service.add_users(users)
        except UserEmailDuplicatedException:
            raise UserEmailDuplicatedException(
                f'Esse {users.username} já está cadastrado com {users.email}.'
            )
