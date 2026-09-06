from uuid import uuid4
from domains.long_term_memory.service import build_memory_namespace
from agents.subgraphs.write_long_term_memory.state import (
    GraphState,
)
from langgraph.runtime import Runtime
import logging

logger = logging.getLogger(__name__)


def write_memory(
    state: GraphState,
    runtime: Runtime,
):
    user_id = runtime.context.user_id
    log_room_id = runtime.context.log_room_id
    log_room_member_id = runtime.context.log_room_member_id
    memories = state["memories"]

    namespace = build_memory_namespace(user_id, log_room_id, log_room_member_id)

    for memory in memories:
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

    logger.info("write_memory 완료")
    logger.debug("장기기억 저장 결과 | results=%s", memories)

    # TODO: 이거 무조건 참이네..? 고쳐야함
    return {"is_saved_long_term_memory": True}
