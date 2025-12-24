from typing import Any

from fastapi import APIRouter

from .deps import CurrentUser
from .schemas import (
    UserPublic,
)

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user
