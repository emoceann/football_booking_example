from typing import Mapping

from src.auth.schemas.user import User
from src.core.serializers.base import BaseSerializer


class UserSerializer(BaseSerializer):
    def serialize(self, data: Mapping) -> User:
        return User.model_validate(data)
