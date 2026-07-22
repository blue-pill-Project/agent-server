import os
from langchain_openrouter import ChatOpenRouter
from common.llm.config import LLMConfig
from common.config import settings


def get_llm(config: LLMConfig):
    OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY

    return ChatOpenRouter(
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        max_retries=config.max_retries,
    )
