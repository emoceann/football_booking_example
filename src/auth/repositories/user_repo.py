from fastapi import Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repositories.base import AbstractUserRepo
from src.auth.schemas.user import User
from src.auth.serializers.user import UserSerializer
from src.core.database.config import get_session


class UserRepo(AbstractUserRepo):
    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            serializer: UserSerializer = Depends()
    ):
        self.session = session
        self.serializer = serializer

    async def create_user(self, data: dict) -> None:
        stmt = text("insert into users(username, password, type) values (:username, :password, :type)").bindparams(
            **data
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_if_exists(self, username: str) -> User:
        stmt = text("select * from users where username = :username").bindparams(username=username)
        res = await self.session.execute(
            stmt
        )
        mapped_result = res.mappings().first()
        if not mapped_result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        return self.serializer.serialize(mapped_result)
