import os
import secrets
from typing import Annotated, Any, Literal

from loguru import logger
from pydantic import (
    AnyUrl,
    BeforeValidator,
    MySQLDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    ENV: Literal["development", "production", "testing"] = "development"
    # Basic
    APP_NAME: str = "FastAPI Starter"
    API_V1_STR: str = "/api/v1"

    # logging
    LOG_SAVE_IN_LOCAL_FILE: bool = True
    LOG_REQUEST_BODY: bool = False
    LOG_RESPONSE_BODY: bool = False
    LOG_BODY_MAX_BYTES: int = 2048
    LOG_BODY_MAX_CONTENT_LENGTH: int = 65536
    LOG_BODY_SKIP_MULTIPART: bool = True

    # security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # cors
    FRONTEND_HOST: str = "http://localhost:3000"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # sqlalchemy
    DB_SCHEME: str = "mysql+pymysql"
    DB_SERVER: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # 如果 scheme 包含 "mysql"，使用 MySQLDsn 构建以保证验证正确
        if "mysql" in self.DB_SCHEME:
            return str(
                MySQLDsn.build(
                    scheme=self.DB_SCHEME,
                    username=self.DB_USER,
                    password=self.DB_PASSWORD,
                    host=self.DB_SERVER,
                    port=self.DB_PORT,
                    path=self.DB_NAME,
                )
            )
        # 对于 PostgreSQL, 可以使用 PostgresDsn.build
        # 否则尝试通用构建，或者直接返回拼接后的字符串
        return f"{self.DB_SCHEME}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"

    # db default user
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    # LLM
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str | None = None

    # 有些配置(如密码)必须非默认值，否则抛出异常
    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENV == "development":
                logger.warning(message)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> "Settings":
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        self._check_default_secret("OPENAI_API_KEY", self.OPENAI_API_KEY)
        return self

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        # 动态选择 .env 文件
        env = os.getenv("ENV", "development")

        # 加载顺序：基础文件在前，环境特定文件在后，local 文件更后（后者覆盖前者）
        env_candidates = [".env", f".env.{env}", ".env.local", f".env.{env}.local"]
        env_files = [path for path in env_candidates if os.path.exists(path)]

        # 如果找到了 .env 文件，通过 _env_file 参数传递
        if env_files and "_env_file" not in kwargs:
            logger.info(f"Loading .env files: {env_files}")
            kwargs["_env_file"] = env_files

        super().__init__(**kwargs)


settings = Settings()
