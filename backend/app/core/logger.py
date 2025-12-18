import logging
import sys

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

        frame = logging.currentframe()
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
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,  # Show full stack trace on exceptions
        diagnose=True,  # Add exception values for easier debugging
    )

    # 保存日志到本地文件
    if settings.LOG_SAVE_IN_LOCAL_FILE:
        logger.add(
            f"logs/{settings.APP_ENV}.log",
            serialize=True,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
        )

    # 将logging的标准日志切换到loguru
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=logging.INFO,
        force=True,
    )

    # 将fastapi的默认日志处理切换到自定义处理
    for logger_name in ("uvicorn", "uvicorn.error", "fastapi"):
        std_logger = logging.getLogger(logger_name)
        std_logger.handlers = []
        std_logger.propagate = True

    # 禁用uvicorn的访问日志(已有自定义的LoggingMiddleware)
    logging.getLogger("uvicorn.access").disabled = True

    # 禁用agent_framework_ag_ui的默认日志
    logging.getLogger("agent_framework_ag_ui").setLevel(logging.CRITICAL)
