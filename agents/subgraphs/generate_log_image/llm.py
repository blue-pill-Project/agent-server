from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

classify_image_category_llm = get_llm(
    LLMConfig(
        model="openai/gpt-5.6-luna",
        temperature=0.7,
    )
)

build_visual_prompt_reference_search_query_llm = get_llm(
    LLMConfig(
        model="openai/gpt-5.6-luna",
        temperature=0.7,
    )
)

build_final_image_prompt_llm = get_llm(
    LLMConfig(
        model="openai/gpt-5.6-luna",
        temperature=0.7,
    )
)
