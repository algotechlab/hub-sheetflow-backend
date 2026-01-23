from typing import List, Union
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto
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
            query = (
                select(
                    User.id,
                    User.username,
                    User.email,
                    User.role,
                    User.created_at,
                    User.updated_at,
                )
                .where(User.is_deleted.__eq__(False))
                .order_by(User.created_at)
            )

            if pagination.filter_by and pagination.filter_value:
                column = getattr(User, pagination.filter_by)
                query = query.where(column.ilike(f'%{pagination.filter_value}%'))

            result = await self.session.execute(query)
            return [UserOutDto.model_validate(row._mapping) for row in result.all()]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def update_user(
        self, user_id: UUID, user_update: UpdateUserDto
    ) -> Union[UserOutDto, None]:
        try:
            update_data = user_update.model_dump(exclude_unset=True)

            stmt = (
                update(User)
                .where(User.id.__eq__(user_id))
                .values(**update_data)
                .returning(User)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_user = result.scalar_one_or_none()

            if updated_user is None:
                return None

            return UserOutDto.model_validate(updated_user)

        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            stmt = (
                update(User)
                .where(User.id.__eq__(user_id), User.is_deleted.__eq__(False))
                .values(is_deleted=True)
                .returning(User)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_user = result.scalar_one_or_none()

            return updated_user is not None
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
