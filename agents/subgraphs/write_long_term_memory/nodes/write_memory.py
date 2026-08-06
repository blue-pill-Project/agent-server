from uuid import uuid4
from domains.long_term_memory.service import build_memory_namespace
from agents.subgraphs.write_long_term_memory.state import (
    GraphState,
)
from langgraph.runtime import Runtime


def write_memory(
    state: GraphState,
    runtime: Runtime,
):
    user_id = runtime.context.user_id
    log_room_id = runtime.context.log_room_id
    log_room_member_id = runtime.context.log_room_member_id

    namespace = build_memory_namespace(user_id, log_room_id, log_room_member_id)

    for memory in state["memories"]:
        memory_id = str(uuid4())
        memory_value = memory.model_dump(
            mode="json",
        )
        runtime.store.put(
            namespace,
            memory_id,
            memory_value,
            index=["content"],
        )

    return {"success": True}
