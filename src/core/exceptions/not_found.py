from src.core.exceptions.base import BaseException_


class NotFound(BaseException_):
    def __init__(
            self,
            message: str,
            *args
    ):
        super().__init__(
            message=message,
            *args
        )
