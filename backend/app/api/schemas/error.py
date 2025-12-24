from enum import Enum
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class APIErrorType(str, Enum):
    """
    错误类型枚举
    用于规范化和标准化错误类型
    只在 HTTPStatus 无法满足时使用
    """

    HTTP_STATUS_ERROR = "HTTP_STATUS_ERROR"  # 默认 HTTP 状态码异常
    VALIDATION_ERROR = "VALIDATION_ERROR"  # 请求参数校验异常


class APIException(HTTPException):
    """
    API 异常基类
    所有自定义的业务异常都应继承自此类
    """

    status_code: HTTPStatus
    error_type: APIErrorType

    def __init__(
        self,
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        detail: str | None = None,
        error_type: APIErrorType = APIErrorType.HTTP_STATUS_ERROR,
        headers: dict[str, str] | None = None,
    ):
        self.error_type = error_type
        super().__init__(
            status_code=status_code,
            detail=detail or status_code.phrase,
            headers=headers,
        )

    @classmethod
    def from_http_exception(cls, exc: HTTPException) -> "APIException":
        return cls(
            status_code=HTTPStatus(exc.status_code),
            detail=exc.detail,
            error_type=APIErrorType.HTTP_STATUS_ERROR,
            headers=getattr(exc, "headers", None),
        )


class APIExceptionResponse(JSONResponse):
    def __init__(
        self,
        exc: APIException,
    ):
        from app.api.schemas.response import APIResponseModel

        super().__init__(
            status_code=exc.status_code,
            content=APIResponseModel[None](
                data=None,
                message=exc.detail,
                error=exc.error_type,
            ).model_dump(),
            headers=exc.headers,
        )
