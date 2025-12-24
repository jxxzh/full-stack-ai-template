import os
import sys

import pymysql
from loguru import logger

# 将项目根目录添加到 python 路径，确保可以导入 app 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings


def create_db() -> None:
    """创建数据库（如果不存在）"""
    if "mysql" not in settings.DB_SCHEME:
        logger.warning(
            f"⚠️ 当前 DB_SCHEME 为 '{settings.DB_SCHEME}'，setup_db.py 脚本主要针对 MySQL 设计。"
        )
        # 如果是 SQLite，通常不需要手动创建数据库文件，或者由 SQLAlchemy 自动处理
        if "sqlite" in settings.DB_SCHEME:
            logger.info("SQLite 数据库将由 SQLAlchemy 自动处理。")
            return

    logger.info(f"正在尝试连接数据库服务器: {settings.DB_SERVER}:{settings.DB_PORT}...")

    try:
        # 注意：此处仍然使用 pymysql，仅适用于 MySQL/MariaDB
        # 如果切换到 PostgreSQL，建议使用相应驱动或修改此逻辑
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
                # 创建数据库
                sql = f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                cursor.execute(sql)
                logger.info(
                    f"✅ 数据库 '{settings.DB_NAME}' 已准备就绪（创建成功或已存在）。"
                )
        finally:
            connection.close()

    except Exception as e:
        logger.error(f"❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 默认设置环境为 development，除非已经指定
    if "ENV" not in os.environ:
        os.environ["ENV"] = "development"

    create_db()
