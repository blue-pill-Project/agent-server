from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

classify_image_category_llm = get_llm(
    LLMConfig(
        model=Models.GPT_LUNA,
        temperature=0.7,
    )
)

build_visual_scene_llm = get_llm(
    LLMConfig(
        model=Models.GPT_LUNA_PRO,
        temperature=0.7,
    )
)
