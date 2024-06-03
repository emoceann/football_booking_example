from src.auth.schemas.token import TokenData
from src.core.serializers.base import BaseSerializer


class TokenSerializer(BaseSerializer):
    def serialize(self, token: str) -> TokenData:
        return TokenData(
            access_token=token
        )
