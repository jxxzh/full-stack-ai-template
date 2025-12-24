"""
SQLModel基础模型类

提供通用的数据库模型基类，包含创建时间和更新时间等常用字段。
"""

from datetime import UTC, datetime
from uuid import UUID, uuid7  # type: ignore[attr-defined]

from sqlmodel import Field, SQLModel

# 软删除使用的时间戳，表示"未删除"状态
# 使用固定的值而不是NULL，以支持联合唯一索引
SOFT_DELETE_DATETIME = datetime(1970, 1, 1, 0, 0, 0, tzinfo=UTC)


class BaseSQLModel(SQLModel):
    """数据库模型基类

    所有业务模型都应该继承此基类，提供通用的字段定义。
    注意：此基类不包含 table=True，具体模型需要自己设置 table=True。
    """

    # 创建时间
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="创建时间",
    )

    # 更新时间
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
        nullable=False,
        description="更新时间",
    )


class BaseUUIDModel(BaseSQLModel):
    id: UUID = Field(default_factory=uuid7, primary_key=True, description="主键ID")


class SoftDeleteModel(BaseSQLModel):
    """软删除模型基类

    提供软删除功能，删除操作不会真正删除数据，而是标记为已删除。
    适配MySQL数据库，支持联合唯一索引。

    使用固定的最小时间戳（1970-01-01 00:00:00 UTC）表示"未删除"状态，
    而不是NULL，这样可以在联合唯一索引中正确工作。
    """

    deleted_at: datetime = Field(
        default=SOFT_DELETE_DATETIME,
        nullable=False,
        description="删除时间，1970-01-01 00:00:00 UTC表示未删除",
    )

    @property
    def is_deleted(self) -> bool:
        """判断是否已被软删除"""
        return self.deleted_at != SOFT_DELETE_DATETIME
