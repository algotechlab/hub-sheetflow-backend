from abc import ABC, abstractmethod
from typing import List, Union
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto


class UsersRepositoriesInterface(ABC):
    @abstractmethod
    async def add_users(self, users: UserBaseDto) -> UserOutDto: ...

    @abstractmethod
    async def list_users(self, pagination: PaginationParamsDTO) -> List[UserOutDto]: ...

    @abstractmethod
    async def update_user(
        self, user_id: UUID, users: UpdateUserDto
    ) -> Union[UserOutDto, None]: ...
