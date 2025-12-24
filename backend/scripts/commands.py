"""项目命令行工具入口"""

import os
import subprocess
import sys


def lint():
    """代码格式化和检查"""
    print("Running ruff check --fix...")  # noqa: T201
    subprocess.run(["ruff", "check", "--fix", "app"], check=False)
    print("Running ruff format...")  # noqa: T201
    subprocess.run(["ruff", "format", "app"], check=False)
    print("Running mypy...")  # noqa: T201
    subprocess.run(["mypy", "app"], check=False)


def dev():
    """启动开发服务器"""
    os.environ["ENV"] = "development"
    os.execvp("fastapi", ["fastapi", "dev"])


def start():
    """启动生产服务器"""
    os.environ["ENV"] = "production"
    os.execvp("fastapi", ["fastapi", "start"])


def migrate_dev():
    """运行数据库迁移（开发环境）"""
    os.environ["ENV"] = "development"
    os.execvp("alembic", ["alembic", "upgrade", "head"])


def migrate_prod():
    """运行数据库迁移（生产环境）"""
    os.environ["ENV"] = "production"
    os.execvp("alembic", ["alembic", "upgrade", "head"])


def make_migrations():
    """生成迁移脚本（开发环境）"""
    os.environ["ENV"] = "development"
    # alembic revision 需要接收额外参数，所以这里用 sys.argv
    args = ["alembic", "revision", "--autogenerate"] + sys.argv[1:]
    os.execvp("alembic", args)


def test():
    """运行测试（testing 环境）"""
    os.environ["ENV"] = "testing"
    # 允许透传 pytest 参数（例如 -k / -q / -x）
    # 通过 `uv run --group test` 确保测试依赖（pytest/httpx 等）已安装
    args = ["uv", "run", "--group", "test", "pytest"] + sys.argv[1:]
    os.execvp("uv", args)
