from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.handlers import api_exception_handler, general_exception_handler
from app.core.logger import setup_logger
from app.core.middlewares import LoggingMiddleware, RequestIDMiddleware
from app.core.schemas import APIError
from app.llm.agent import create_agent
from app.llm.chat_client import get_chat_client
from app.routes import health

# 初始化日志
setup_logger()


app = FastAPI()

# 添加中间件 - 注意顺序很重要！
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注意：FastAPI/Starlette 中间件是“后添加先执行”（最后 add 的在最外层）。
# 因此要让 RequestIDMiddleware 先执行并写入 request.state.request_id，
# 需要先添加 LoggingMiddleware，再添加 RequestIDMiddleware。
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# 添加异常处理器
app.add_exception_handler(APIError, api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# 添加路由
app.include_router(health.router)

my_agent = create_agent(get_chat_client())

add_agent_framework_fastapi_endpoint(
    app=app,
    agent=my_agent,
    path="/agent",
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FastAPI Starter"}
