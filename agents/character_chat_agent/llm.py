from common.llm.factory import get_llm
from common.llm.config import LLMConfig
from common.llm.models import Models
from agents.character_chat_agent.tools.phone.tool import use_phone

tools = [
    use_phone,
]

generate_reply_llm = get_llm(
    LLMConfig(
        model=Models.GPT_LUNA_PRO,
        temperature=1.0,
    )
)

character_llm = generate_reply_llm.bind_tools(tools)
