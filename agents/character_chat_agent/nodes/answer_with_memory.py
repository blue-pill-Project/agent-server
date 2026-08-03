from langgraph.runtime import Runtime

from agents.character_chat_agent.llm import generate_reply_llm
from agents.character_chat_agent.state import Context, GraphState
from agents.character_chat_agent.prompts import generate_reply_with_memory_instructions


def answer_with_memory(state: GraphState, runtime: Runtime[Context]) -> dict:
    query = state["messages"][-1].content

    namespace = (
        "memories",
        runtime.context.log_room_id,
        runtime.context.log_room_member_id,
        runtime.context.user_id,
    )

    memories = runtime.store.search(namespace, query=query, limit=5)
    retrieved_memories = [memory.value for memory in memories]

    formatted_system_prompt = generate_reply_with_memory_instructions.format(
        log_room_member_prompt=runtime.context.log_room_member_prompt,
        log_room_relationships=runtime.context.log_room_relationships,
        retrieved_memories=retrieved_memories,
    )

    messages = [
        {"role": "system", "content": formatted_system_prompt},
        *state["messages"],
    ]

    reply = generate_reply_llm.invoke(messages)

    return {
        "retrieved_memories": retrieved_memories,
        "messages": [{"role": "assistant", "content": reply.content}],
    }