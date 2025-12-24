from collections.abc import AsyncGenerator, Generator

import httpx
import pymysql
import pytest
from alembic.config import Config as AlembicConfig
from loguru import logger
from sqlmodel import Session

from alembic import command as alembic_command
from app.api.deps import get_db
from app.core.config import settings
from app.core.db import SessionLocal
from app.main import app


def _assert_testing_db() -> None:
    """
    防误连保护：
    - 必须通过 `uv run test`（或显式设置 ENV=testing）启动
    - DB_NAME 必须包含 `_test`
    """

    logger.info(f"ENVIRONMENT: {settings.ENV}")
    if settings.ENV != "testing":
        raise RuntimeError(
            "当前并非 testing 环境（ENV!=testing）。请使用 `uv run test` 运行测试。"
        )

    if "_test" not in settings.DB_NAME:
        raise RuntimeError(
            "DB_NAME 必须包含 `_test` 以避免误写入非测试库。"
            f"当前为: {settings.DB_NAME}。"
            "请在 `env.testing` / `.env.testing` 中配置测试库（例如 fastapi_starter_test）。"
        )


def _run_alembic_upgrade_head() -> None:
    alembic_cfg = AlembicConfig("alembic.ini")
    # 关键：覆盖 DB URL，确保迁移运行在 testing 的固定测试库上
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))
    alembic_command.upgrade(alembic_cfg, "head")


def _ensure_test_database_exists() -> None:
    """
    确保固定测试库存在：
    - 仅在通过 `_assert_testing_db()` 后才允许创建
    - 使用 `CREATE DATABASE IF NOT EXISTS`，避免破坏已有测试库
    """

    connection = pymysql.connect(
        host=settings.DB_SERVER,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        connection.commit()
    finally:
        connection.close()


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_db() -> None:
    _assert_testing_db()
    _ensure_test_database_exists()
    _run_alembic_upgrade_head()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


@pytest.fixture
def override_get_db(db_session: Session) -> Generator[None, None, None]:
    def _override() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
async def client(override_get_db: None) -> AsyncGenerator[httpx.AsyncClient, None]:  # noqa: ARG001
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
