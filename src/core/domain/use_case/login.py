from argon2 import PasswordHasher
from src.core.domain.dtos.login import LoginDTO
from src.core.domain.service.login import LoginService
from src.core.domain.utils.get_argon import verify_password
from src.core.exceptions.custom import DatabaseException


class LoginUseCase:
    def __init__(self, login_service: LoginService):
        self.login_service = login_service

    async def login(self, login_dto: LoginDTO):
        try:
            user = await self.login_service.get_user_by_email(login_dto.email)

            if not user:
                raise DatabaseException('Invalid email or password')

            ph = PasswordHasher()
            try:
                ph.verify(user['password'], login_dto.password)
            except Exception:
                raise DatabaseException('Invalid email or password')

            if not verify_password(user['password'], login_dto.password):
                raise DatabaseException('Invalid email or password')

            return await self.login_service.login(login_dto)
        except Exception as error:
            raise DatabaseException(str(error))
