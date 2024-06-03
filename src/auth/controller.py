from datetime import timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, ExpiredSignatureError
from passlib.hash import bcrypt

from src.auth.repositories.user_repo import UserRepo
from src.auth.schemas.token import TokenData
from src.auth.schemas.user import UserIn
from src.auth.serializers.token import TokenSerializer
from src.auth.utils.auth_tools import check_password, create_access_token
from src.core.settings import get_settings, Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthController:
    def __init__(
            self,
            settings: Settings = Depends(get_settings),
            repo: UserRepo = Depends(),
            token_serializer: TokenSerializer = Depends()
    ):
        self.settings = settings
        self.repo = repo
        self.token_serializer = token_serializer

    async def get_current_user(
            self,
            token: str
    ):
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCRYPT_ALGORITHM]
            )
            user = await self.repo.get_user_if_exists(payload.get("username"))
            return user
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Expired token')
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')

    async def check_credentials(
            self,
            user_data: OAuth2PasswordRequestForm
    ) -> TokenData:
        user = await self.repo.get_user_if_exists(user_data.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        if not check_password(user.password, user_data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        return self.token_serializer.serialize(
            create_access_token(
                user.model_dump(exclude={"id", "password"}),
                expires_delta=timedelta(seconds=self.settings.JWT_EXPIRE_SECONDS)
            )
        )

    async def create_user(
            self,
            data: UserIn
    ) -> None:
        data.password = bcrypt.hash(data.password)
        return await self.repo.create_user(data.model_dump())
