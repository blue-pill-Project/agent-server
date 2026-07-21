from langgraph.runtime import Runtime

from ..state import GraphState, Context


def load_long_term_memories(
    state: GraphState,
    runtime: Runtime[Context],
):
    namespace = (
        "memories",
        runtime.context.log_room_id,
        runtime.context.log_room_member_id,
        runtime.context.user_id,
    )

    query = """
    오늘 하루 계획을 만들 때 참고할 유저 선호, 캐릭터 관계, 반복 설정, 중요한 장기기억
    """

    memories = runtime.store.search(
        namespace,
        query=query,
        limit=10,
    )

    return {
        "long_term_memories": [memory.value for memory in memories],
    }
