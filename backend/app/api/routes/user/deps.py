from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.api.deps import SessionDep
from app.api.routes.auth.deps import TokenDep
from app.api.routes.auth.schemas import TokenPayload
from app.api.routes.auth.service import ALGORITHM
from app.api.routes.user.models import User
from app.api.schemas.error import APIException
from app.core.config import settings


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise APIException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.get(User, UUID(token_data.sub))  # 显式将 sub 转换为 UUID
    if not user:
        raise APIException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise APIException(status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise APIException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
