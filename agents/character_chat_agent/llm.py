from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

generate_reply_llm = get_llm(
    LLMConfig(
        model="openai/gpt-5.6-luna",
        temperature=0.7,
    )
)
