from enum import Enum

from agent_framework import ChatClientProtocol
from agent_framework.openai import OpenAIChatClient

from app.core.config import settings


class ChatClientContext(Enum):
    PLUS = "plus"
    FLASH = "flash"
    MAX = "max"


def get_chat_client(
    context: ChatClientContext = ChatClientContext.PLUS,
) -> ChatClientProtocol:
    model_id: str

    match context:
        case ChatClientContext.PLUS:
            model_id = "qwen-plus"
        case ChatClientContext.FLASH:
            model_id = "qwen-flash"
        case ChatClientContext.MAX:
            model_id = "qwen-max"

    return OpenAIChatClient(
        model_id=model_id,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
