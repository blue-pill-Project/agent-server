from agents.character_chat_agent.llm import generate_reply_llm
from agents.character_chat_agent.state import GraphState
from agents.character_chat_agent.prompts import (
    generate_reply_system_instructions,
)
from langgraph.runtime import Runtime
from agents.character_chat_agent.state import Context


def generate_reply(state: GraphState, runtime: Runtime[Context]) -> dict:
    log_room_member_prompt = runtime.context.log_room_member_prompt
    log_room_relationships = runtime.context.log_room_relationships

    formatted_system_prompt = generate_reply_system_instructions.format(
        log_room_member_prompt=log_room_member_prompt,
        log_room_relationships=log_room_relationships,
    )

    messages = [
        {
            "role": "system",
            "content": formatted_system_prompt,
        },
        *state["messages"],
    ]

    response = generate_reply_llm.invoke(messages)

    return {
        "messages": [
            {
                "role": "assistant",
                "content": response.content,
            }
        ]
    }
