from datetime import datetime, timedelta

import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.login import LoginDTO, LoginResponseDTO
from src.core.domain.interface.login import LoginRepositoriesInterface
from src.core.domain.models.users import User
from src.core.domain.utils.get_argon import verify_password
from src.core.exceptions.custom import DatabaseException

SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'


class LoginRepositoryPostgres(LoginRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str):
        try:
            stmt = select(User).where(User.email.__eq__(email))
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                return None

            return {
                'id': user.id,
                'email': user.email,
                'password': user.password,
                'role': user.role,
            }
        except Exception as error:
            raise DatabaseException(str(error))

    async def login(self, login_dto: LoginDTO) -> str:
        try:
            stmt = select(User).where(User.email.__eq__(login_dto.email))
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                raise DatabaseException('Invalid email or password')

            if not verify_password(user.password, login_dto.password):
                raise DatabaseException('Invalid email or password')

            payload = {
                'sub': str(user.id),
                'email': user.email,
                'role': user.role,
                'exp': datetime.now() + timedelta(hours=1),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            return LoginResponseDTO(
                email=user.email,
                password=login_dto.password,
                user_id=user.id,
                token=token,
                role=user.role,
            )
        except Exception as error:
            raise DatabaseException(str(error))
