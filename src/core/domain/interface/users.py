from abc import ABC, abstractmethod

from src.core.domain.dtos.users import UserBaseDto, UserOutDto


class UsersRepositoriesInterface(ABC):
    @abstractmethod
    async def add_users(self, users: UserBaseDto) -> UserOutDto: ...
