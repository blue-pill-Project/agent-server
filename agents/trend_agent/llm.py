from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

filter_results_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_LATEST,
        temperature=0.1,
    )
)


extract_trends_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_LATEST,
        temperature=0.1,
    )
)