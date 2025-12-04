from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import (
    DuplicatedException,
    UserEmailDuplicatedException,
)
from src.core.domain.interface.users import UsersRepositoriesInterface
from src.core.domain.models.users import User
from src.core.exceptions.custom import DatabaseException
from src.infrastructure.database.utils import PostgresErrorCode


class UsersRepositoryPostgres(UsersRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_users(self, users: UserBaseDto) -> UserOutDto:
        try:
            user = User(**users.model_dump())
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return UserOutDto.model_validate(user)
        except IntegrityError as error:
            await self.session.rollback()
            orig = error.orig
            if orig is None or not hasattr(orig, 'pgcode'):
                raise DuplicatedException(str(error))

            error_code = orig.pgcode
            detail = str(orig)

            match error_code:
                case PostgresErrorCode.UNIQUE_VIOLATION:
                    if 'email' in detail:
                        raise UserEmailDuplicatedException()

            raise DuplicatedException(str(error))
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def list_users(self, pagination: PaginationParamsDTO) -> List[UserOutDto]:
        try:
            query = select(
                User.id,
                User.username,
                User.email,
                User.role,
                User.created_at,
                User.updated_at,
            ).order_by(User.created_at)

            if pagination.filter_by and pagination.filter_value:
                query = query.filter(
                    getattr(User, pagination.filter_by).__eq__(pagination.filter_value)
                )
            result = await self.session.execute(query)
            return [UserOutDto.model_validate(row._mapping) for row in result.all()]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
