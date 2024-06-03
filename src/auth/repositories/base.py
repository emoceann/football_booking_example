from abc import ABC, abstractmethod

from src.auth.schemas.user import User


class AbstractUserRepo(ABC):
    @abstractmethod
    async def create_user(self, data: dict) -> ...:
        raise NotImplementedError

    @abstractmethod
    async def get_user_if_exists(self, username: str) -> User:
        raise NotImplementedError
