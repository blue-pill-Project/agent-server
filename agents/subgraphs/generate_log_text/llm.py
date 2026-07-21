from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

generate_log_text_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_LATEST,
        temperature=1.0,
    )
)
