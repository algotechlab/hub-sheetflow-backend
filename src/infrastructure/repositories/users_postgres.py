from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
            error_code = error.orig.pgcode
            detail = str(error.orig)
            match error_code:
                case PostgresErrorCode.UNIQUE_VIOLATION:
                    if 'email' in detail:
                        raise UserEmailDuplicatedException()

            raise DuplicatedException(str(error))
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
