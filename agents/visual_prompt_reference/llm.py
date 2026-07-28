from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models


extract_prompt_from_image_llm = get_llm(
    LLMConfig(
        model="google/gemini-3.6-flash",
        temperature=1,
    )
)


extract_situation_from_image_llm = get_llm(
    LLMConfig(
        model="google/gemini-3.6-flash",
        temperature=0.3,
    )
)
