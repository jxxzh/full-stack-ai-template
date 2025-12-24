from pydantic import EmailStr
from sqlmodel import Field, SQLModel, UniqueConstraint

from app.api.models import BaseUUIDModel, SoftDeleteModel


class UserBase(SQLModel):
    is_superuser: bool = Field(default=False, description="是否超级用户")
    is_active: bool = Field(default=True, description="是否激活")
    email: EmailStr = Field(max_length=255, description="用户邮箱")
    full_name: str | None = Field(default=None, max_length=255, description="用户全名")
    avatar_url: str | None = Field(default=None, max_length=500, description="头像URL")


# 数据库模型，表名对应类名
# 最先继承的模型的字段在数据库表的DDL中在最后面
class User(UserBase, SoftDeleteModel, BaseUUIDModel, table=True):
    __table_args__ = (
        UniqueConstraint("email", "deleted_at", name="uk_user_email_deleted_at"),
    )

    hashed_password: str = Field(max_length=255, description="加密后的密码")
