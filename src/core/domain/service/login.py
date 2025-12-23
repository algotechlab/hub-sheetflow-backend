from src.core.domain.dtos.login import LoginDTO
from src.core.domain.interface.login import LoginRepositoriesInterface


class LoginService:
    def __init__(self, repository: LoginRepositoriesInterface):
        self.repository = repository

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def login(self, login_dto: LoginDTO) -> str | None:
        return await self.repository.login(login_dto)
