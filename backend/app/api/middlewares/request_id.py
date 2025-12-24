import uuid

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    专门负责生成和管理 request_id 的中间件
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 始终由服务端生成唯一的 request_id，不信任客户端传入的 header
        request_id = str(uuid.uuid7())  # type: ignore[attr-defined]
        request.state.request_id = request_id

        # 使用 contextualize，使得该请求生命周期内的所有日志（包括框架日志）都能访问到 request_id
        with logger.contextualize(req_id=request_id):
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
