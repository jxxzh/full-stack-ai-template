from sqlalchemy import event
from sqlalchemy.orm import ORMExecuteState, sessionmaker, with_loader_criteria
from sqlmodel import Session, create_engine, select

from app.api.models import SOFT_DELETE_DATETIME, SoftDeleteModel
from app.api.routes.user.models import User
from app.api.routes.user.schemas import UserCreate
from app.api.routes.user.service import create_user
from app.core import (
    models as _models,  # noqa: F401  # 导入所有 table=True 模型以确保映射已注册
)
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28

SessionLocal = sessionmaker(bind=engine, class_=Session)


def _iter_subclasses(cls: type) -> list[type]:
    """递归获取所有子类（包含多层继承）。"""

    def _walk(cur: type) -> list[type]:
        subs = list(cur.__subclasses__())
        return subs + [g for s in subs for g in _walk(s)]

    # 去重且保持稳定顺序
    seen: set[type] = set()
    ordered: list[type] = []
    for c in _walk(cls):
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def _soft_delete_mapped_models() -> list[type]:
    """获取所有继承自 SoftDeleteModel 且确实映射为表（table=True）的模型类。"""

    def _is_mapped_table_model(model: type) -> bool:
        return hasattr(model, "__table__") and hasattr(model, "__mapper__")

    return [m for m in _iter_subclasses(SoftDeleteModel) if _is_mapped_table_model(m)]


_SOFT_DELETE_MODELS: tuple[type, ...] = tuple(_soft_delete_mapped_models())


@event.listens_for(SessionLocal, "do_orm_execute")
def _add_filtering_criteria(execute_state: ORMExecuteState):
    """
    自动为查询添加软删除过滤条件。
    可以通过 `execution_options({"include_deleted": True})` 来禁用此过滤。
    """
    if not execute_state.is_select:
        return
    if execute_state.execution_options.get("include_deleted", False):
        return
    # 如果执行的是列加载，则不添加软删除过滤条件
    # 列加载是指在查询中加载某个字段，而不是查询整个表
    if execute_state.is_column_load:
        return

    # SoftDeleteModel 本身不是映射表（非 table=True），不能直接作为 with_loader_criteria 的 entity。
    # 这里对所有继承 SoftDeleteModel 的“实际表模型”逐个追加过滤条件。
    stmt = execute_state.statement
    for model in _SOFT_DELETE_MODELS:
        stmt = stmt.options(
            with_loader_criteria(
                model,
                lambda cls: cls.deleted_at == SOFT_DELETE_DATETIME,
                include_aliases=True,
            )
        )
    execute_state.statement = stmt


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    superuser = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not superuser:
        superuser_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = create_user(session=session, user_create=superuser_in)
