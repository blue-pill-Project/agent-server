import uuid
from agents.character_chat_agent.state import Context, GraphState
from langgraph.runtime import Runtime


def store_long_term_memory(
    state: GraphState,
    runtime: Runtime[Context],
):
    decision = state["memory_decision"]

    memory_id = str(uuid.uuid4())

    namespace = (
        "memories",
        runtime.context.log_room_id,
        runtime.context.log_room_member_id,
        runtime.context.user_id,
    )

    memory = {
        "data": decision.content,
    }

    runtime.store.put(
        namespace,
        memory_id,
        memory,
    )

    return {
        "stored_memory_id": memory_id,
    }
