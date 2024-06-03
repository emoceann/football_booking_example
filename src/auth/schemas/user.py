from pydantic import BaseModel

from src.auth.constants.user_types import ALLOWED_USER_TYPES


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str
    type: ALLOWED_USER_TYPES


class User(UserIn):
    id: int
    password: str
    type: ALLOWED_USER_TYPES
