from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

generate_reply_llm = get_llm(
    LLMConfig(
        # model="sao10k/l3.1-euryale-70b",
        # model="z-ai/glm-5.3-flash",
        # model="anthracite-org/magnum-v4-72b",
        # model="deepseek/deepseek-v4-flash-0731",
        # model="anthropic/claude-opus-5",
        model="openai/gpt-5.6-luna",
        temperature=1.0,
    )
)


classify_intent_llm = get_llm(
    LLMConfig(
        model=Models.GPT_LUNA,
        temperature=0.7,
    )
)
