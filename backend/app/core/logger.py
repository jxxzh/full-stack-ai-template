import logging
import sys
from types import FrameType

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """
    重定向logging的默认日志处理到loguru
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename in {logging.__file__, __file__}:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger() -> None:
    """
    设置日志记录器
    """

    logger.remove()  # 移除默认的handler
    # 添加控制台handler
    logger.add(
        sys.stderr,
        colorize=True,
        backtrace=True,  # Show full stack trace on exceptions
        diagnose=True,  # Add exception values for easier debugging
    )

    # 保存日志到本地文件
    if settings.LOG_SAVE_IN_LOCAL_FILE:
        logger.add(
            f"logs/{settings.ENV}.log",
            serialize=True,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
        )

    # 将 logging 的标准日志切换到 loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # 清除所有已存在的 logger 的 handler，并设置它们向上传播到 root logger
    # 这样它们都会被 root logger 的 InterceptHandler 拦截并转发给 loguru
    for name in logging.root.manager.loggerDict.keys():
        std_logger = logging.getLogger(name)
        std_logger.handlers = []
        std_logger.propagate = True

    # 禁用 uvicorn 的访问日志，因为我们已经有了自定义的 LoggingMiddleware
    logging.getLogger("uvicorn.access").disabled = True
