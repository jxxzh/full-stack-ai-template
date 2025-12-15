from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.core.schemas import APIErrorType


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    全局通用异常处理器
    """
    request_id = getattr(request.state, "request_id", "N/A")
    logger.exception("Unhandled exception occurred", extra={"request_id": request_id})
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "message": str(exc),
            "error": APIErrorType.INTERNAL_SERVER_ERROR.value,
            "request_id": request_id,
        },
    )
