import os
from typing import Literal

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Basic
    APP_ENV: Literal["development", "production", "testing"] = "development"
    APP_NAME: str = "FastAPI Starter"

    # logging
    LOG_SAVE_IN_LOCAL_FILE: bool = True
    LOG_REQUEST_BODY: bool = False
    LOG_RESPONSE_BODY: bool = False
    LOG_BODY_MAX_BYTES: int = 2048
    LOG_BODY_MAX_CONTENT_LENGTH: int = 65536
    LOG_BODY_SKIP_MULTIPART: bool = True

    # LLM
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        # 动态选择 .env 文件
        env = os.getenv("ENV", "development")
        env_candidates = [".env", f".env.{env}", ".env.local"]
        env_files = [path for path in env_candidates if os.path.exists(path)]

        # 如果找到了 .env 文件，通过 _env_file 参数传递
        if env_files and "_env_file" not in kwargs:
            logger.info(f"Loading .env files: {env_files}")
            kwargs["_env_file"] = env_files

        super().__init__(**kwargs)


settings = Settings()
