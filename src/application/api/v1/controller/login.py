from src.application.api.v1.schemas.login import LoginInSchema
from src.core.domain.dtos.login import LoginDTO
from src.core.domain.use_case.login import LoginUseCase


class LoginController:
    def __init__(self, use_case: LoginUseCase):
        self.use_case = use_case

    async def login(self, login: LoginInSchema) -> str:
        login_dto = LoginDTO(
            **login.model_dump()
        )  # Ensure it's an instance of LoginDTO
        return await self.use_case.login(login_dto)
