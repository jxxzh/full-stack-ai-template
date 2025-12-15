from collections.abc import Callable
from functools import wraps

from starlette.requests import Request
from starlette.responses import Response


def response_wrapper(func: Callable):
    """
    一个装饰器，用于将路由函数的返回值自动包装在标准的成功响应体中。
    被装饰的函数必须将 `request: Request` 作为其关键字参数之一。
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if not isinstance(request, Request):
            raise TypeError(
                "The decorated function must have a 'request: Request' "
                "keyword argument."
            )
        data = await func(*args, **kwargs)
        if isinstance(data, Response):
            return data
        return {
            "data": data,
            "message": "操作成功",
            "request_id": getattr(request.state, "request_id", "N/A"),
        }

    return wrapper
