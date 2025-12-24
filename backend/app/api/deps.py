from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
