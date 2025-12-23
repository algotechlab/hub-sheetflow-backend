from abc import ABC, abstractmethod

from src.core.domain.dtos.login import LoginDTO


class LoginRepositoriesInterface(ABC):
    @abstractmethod
    async def login(self, login: LoginDTO) -> str | None: ...

    @abstractmethod
    async def get_user_by_email(self, email: str): ...
