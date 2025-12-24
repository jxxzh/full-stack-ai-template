"""
SQLModel 模型注册入口（用于 Alembic autogenerate）

Alembic 生成迁移时依赖 `SQLModel.metadata`。
只有在导入了所有 `table=True` 的模型后，这些表才会注册到 metadata 中。

约定：把所有业务表模型在这里集中导入（仅为了 side-effect 注册）。
"""

# ruff: noqa: F401

from app.api.routes.user.models import User
