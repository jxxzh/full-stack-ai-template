from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.handlers import general_exception_handler
from app.api.main import api_router
from app.api.middlewares import LoggingMiddleware, RequestIDMiddleware
from app.core.config import settings
from app.core.logger import setup_logger
from app.llm.agent import create_agent
from app.llm.chat_client import get_chat_client

# 初始化日志配置
setup_logger()

app = FastAPI(
    # 生产环境不暴露 OpenAPI 接口
    openapi_url=None if settings.ENV == "production" else "/openapi.json",
)


# 添加中间件 - 注意顺序很重要！
# cors中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# 注意：FastAPI/Starlette 中间件是“后添加先执行”（最后 add 的在最外层）。
# 因此要让 RequestIDMiddleware 先执行并写入 request.state.request_id，
# 需要先添加 LoggingMiddleware，再添加 RequestIDMiddleware。
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


# 添加异常处理器
app.add_exception_handler(RequestValidationError, general_exception_handler)
app.add_exception_handler(HTTPException, general_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# 添加路由
app.include_router(api_router, prefix=settings.API_V1_STR)

my_agent = create_agent(get_chat_client())

add_agent_framework_fastapi_endpoint(
    app=app,
    agent=my_agent,
    path=f"{settings.API_V1_STR}/agent",
)
