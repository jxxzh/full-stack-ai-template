import json
import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings
from app.core.logger import logger


def _preview_bytes(data: bytes, *, limit: int) -> dict[str, Any]:
    data_len = len(data)
    if data_len <= limit:
        return {
            "size": data_len,
            "truncated": False,
            "preview": data.decode("utf-8", errors="replace"),
        }
    return {
        "size": data_len,
        "truncated": True,
        "preview": data[:limit].decode("utf-8", errors="replace"),
    }


def _build_request_log_payload(request: Request) -> dict[str, Any]:
    content_type = request.headers.get("content-type")
    return {
        "method": request.method,
        "path": request.url.path,
        "query": request.url.query,
        "content_type": content_type,
        "content_length": request.headers.get("content-length"),
        "client": getattr(request.client, "host", None),
    }


def _should_log_body(*, content_type: str | None, content_length: str | None) -> bool:
    if (
        settings.LOG_BODY_SKIP_MULTIPART
        and content_type
        and "multipart/form-data" in content_type
    ):
        return False
    if content_length is None:
        return True
    try:
        return int(content_length) <= settings.LOG_BODY_MAX_CONTENT_LENGTH
    except ValueError:
        return True


def _build_response_log_payload(response: Response) -> dict[str, Any]:
    content_type = response.headers.get("content-type")
    payload: dict[str, Any] = {
        "status_code": response.status_code,
        "content_type": content_type,
        "content_length": response.headers.get("content-length"),
    }

    body = getattr(response, "body", None)
    if isinstance(body, (bytes, bytearray)):
        if settings.LOG_RESPONSE_BODY and _should_log_body(
            content_type=content_type,
            content_length=payload["content_length"],
        ):
            payload["body"] = _preview_bytes(
                bytes(body), limit=settings.LOG_BODY_MAX_BYTES
            )
        else:
            payload["body"] = {"size": len(body), "truncated": None}
    return payload


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    专门负责请求日志记录的中间件
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = getattr(request.state, "request_id", "N/A")
        start_time = time.perf_counter()

        request_payload = _build_request_log_payload(request)
        if settings.LOG_REQUEST_BODY and _should_log_body(
            content_type=request_payload["content_type"],
            content_length=request_payload["content_length"],
        ):
            request_body_bytes = await request.body()
            if request_body_bytes:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    try:
                        request_payload["body"] = json.loads(request_body_bytes)
                    except json.JSONDecodeError:
                        request_payload["body"] = _preview_bytes(
                            request_body_bytes, limit=settings.LOG_BODY_MAX_BYTES
                        )
                else:
                    request_payload["body"] = _preview_bytes(
                        request_body_bytes, limit=settings.LOG_BODY_MAX_BYTES
                    )
        else:
            request_payload["body"] = None

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000
        # 设置请求头
        response.headers["X-Process-Time"] = str(process_time)

        response_payload = _build_response_log_payload(response)

        logger.bind(
            req_id=request_id,
            req=request_payload,
            resp=response_payload,
        ).info(
            f"{request.method} {request.url.path}: {response.status_code} ({process_time:.2f}ms)"
        )

        return response
