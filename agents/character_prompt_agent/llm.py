from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

generate_character_prompt_llm = get_llm(
    LLMConfig(
        model=Models.GEMINI_FLASH_LITE,
        temperature=0.7,
    )
)
