from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models

build_retrieval_query_llm = get_llm(
    LLMConfig(
        # NOTE: luna가 지금 제일 저렴하고 성능이 좋아보임
        # model="openai/gpt-5.6-luna",
        # model="openai/gpt-5.6-terra",
        # model="openai/gpt-oss-120b",
        model="openai/gpt-5.6-luna-pro",
        temperature=1,
    )
)
