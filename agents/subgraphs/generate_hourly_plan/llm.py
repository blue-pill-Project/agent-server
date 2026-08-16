from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

generate_hourly_plan_llm = get_llm(
    LLMConfig(
        model="z-ai/glm-4.6v",
        temperature=0.7,
    )
)
