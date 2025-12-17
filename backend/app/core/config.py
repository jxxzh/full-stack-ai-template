import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Starter"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT_JSON: bool = True

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        # 动态选择 .env 文件
        env = os.getenv("ENV", "development")
        env_candidates = [".env", f".env.{env}"]
        env_files = [path for path in env_candidates if os.path.exists(path)]

        # 如果找到了 .env 文件，通过 _env_file 参数传递
        if env_files and "_env_file" not in kwargs:
            logger.info(f"Loading .env files: {env_files}")
            kwargs["_env_file"] = env_files

        super().__init__(**kwargs)


# 单例模式的 settings 实例
_settings: Settings | None = None


def get_settings() -> Settings:
    """获取 settings 实例（单例模式，延迟初始化）"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """重新加载 settings 实例（用于环境切换）"""
    global _settings
    _settings = Settings()
    return _settings


# 导出 settings 实例以保持向后兼容
settings = get_settings()
