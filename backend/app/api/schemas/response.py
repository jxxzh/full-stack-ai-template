from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from .error import APIErrorType

T = TypeVar("T")


class APIResponseModel(BaseModel, Generic[T]):
    """
    统一 API 响应体模型
    """

    data: T = Field(description="成功时返回的数据")
    message: str = Field(default="OK", description="接口操作结果的说明，成功失败都返回")
    error: APIErrorType | None = Field(
        default=None, description="错误类型枚举值，仅在失败时返回"
    )
    # 已经在请求头中返回了，这里不再返回 request_id
    # request_id: str = Field(..., description="请求的唯一标识符，用于链路追踪")
