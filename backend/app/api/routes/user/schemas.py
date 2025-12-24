from typing import Annotated
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from .models import UserBase

# 定义常用的字段类型，以便复用
_EmailField = Annotated[EmailStr, Field(max_length=255)]
_FullNameField = Annotated[str | None, Field(default=None, max_length=255)]
_AvatarUrlField = Annotated[str | None, Field(default=None, max_length=500)]
_PasswordField = Annotated[str, Field(min_length=8, max_length=32)]


class UserCreate(UserBase):
    password: _PasswordField


class UserRegister(SQLModel):
    email: _EmailField
    password: _PasswordField
    full_name: _FullNameField
    avatar_url: _AvatarUrlField = None


class UserUpdate(UserBase):
    email: _EmailField | None = None  # type: ignore
    password: _PasswordField | None = None


class UserUpdateMe(SQLModel):
    full_name: _FullNameField | None = None
    email: _EmailField | None = None
    avatar_url: _AvatarUrlField | None = None


class UpdatePassword(SQLModel):
    current_password: _PasswordField
    new_password: _PasswordField


class UserPublic(UserBase):
    id: UUID
