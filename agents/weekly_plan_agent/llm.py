from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

select_trends_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_LATEST,
        temperature=0.1,
    )
)

generate_weekly_plan_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_LATEST,
        temperature=0.1,
    )
)
