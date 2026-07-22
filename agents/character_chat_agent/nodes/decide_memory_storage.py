from agents.character_chat_agent.llm import generate_reply_llm
from agents.character_chat_agent.state import GraphState, MemoryDecision
from agents.character_chat_agent.prompts import (
    decide_memory_storage_instructions,
)


def decide_memory_storage(state: GraphState) -> dict:

    last_message = state["messages"][-1]
    content = last_message.content

    formatted_prompt = decide_memory_storage_instructions.format(
        content=content,
    )

    structured_model = generate_reply_llm.with_structured_output(MemoryDecision)

    response = structured_model.invoke(formatted_prompt)

    return {"memory_decision": response}
