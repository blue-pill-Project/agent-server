from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models


extract_info_from_image_llm = get_llm(
    LLMConfig(
        model=Models.GPT_LUNA,
        temperature=1,
    )
)
