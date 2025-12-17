import sys

from loguru import logger

from app.core.config import settings


def setup_logger():
    """
    Set up the logger with console and optional file handlers.
    """
    logger.remove()  # Remove the default handler to prevent duplicates

    # Add a console handler with colors and a rich format
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <4}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,  # Show full stack trace on exceptions
        diagnose=True,  # Add exception values for easier debugging
    )

    # If JSON logging is enabled, add a file handler
    if settings.LOG_FORMAT_JSON:
        logger.add(
            f"logs/{settings.APP_ENV}.log",
            serialize=True,  # Output logs in JSON format
            rotation="10 MB",  # Rotate the log file when it reaches 10 MB
            retention="7 days",  # Keep logs for up to 7 days
            compression="zip",  # Compress rotated log files
            backtrace=True,
            diagnose=True,
        )
