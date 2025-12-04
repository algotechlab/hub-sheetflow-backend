from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UserBaseDto, UserOutDto


class UsersRepositoriesInterface(ABC):
    @abstractmethod
    async def add_users(self, users: UserBaseDto) -> UserOutDto: ...

    @abstractmethod
    async def list_users(self, pagination: PaginationParamsDTO) -> List[UserOutDto]: ...
