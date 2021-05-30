class MobileRequiredException(Exception):

    def __init__(self, message='手机号必填') -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class InternalServerError(Exception):

    def __init__(self, message='服务端异常') -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class BadRequest(Exception):

    def __init__(self, message='请求出错，请先检查参数') -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message