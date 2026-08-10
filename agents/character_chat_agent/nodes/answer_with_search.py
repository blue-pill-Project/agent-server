import json
import urllib.parse
import urllib.request

from langgraph.runtime import Runtime

from agents.character_chat_agent.llm import generate_reply_llm
from agents.character_chat_agent.state import Context, GraphState
from agents.character_chat_agent.prompts import generate_reply_with_search_instructions
from common.config import settings


def answer_with_search(state: GraphState, runtime: Runtime[Context]) -> dict:
    query = state["messages"][-1].content

    enc_text = urllib.parse.quote(query)
    url = (
        f"https://openapi.naver.com/v1/search/blog?query={enc_text}&display=5&sort=sim"
    )

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)

    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode("utf-8"))
    search_results = result.get("items", [])

    formatted_system_prompt = generate_reply_with_search_instructions.format(
        log_room_member_prompt=runtime.context.log_room_member_prompt,
        log_room_relationships=runtime.context.log_room_relationships,
        search_results=search_results,
    )

    messages = [
        {"role": "system", "content": formatted_system_prompt},
        *state["messages"],
    ]

    reply = generate_reply_llm.invoke(messages)

    return {
        "search_results": search_results,
        "messages": [{"role": "assistant", "content": reply.content}],
    }
