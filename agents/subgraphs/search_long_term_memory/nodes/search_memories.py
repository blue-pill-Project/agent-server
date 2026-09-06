import logging

from agents.subgraphs.search_long_term_memory.state import (
    GraphState,
    Context,
    SearchResult,
)
from langgraph.runtime import Runtime
from domains.long_term_memory.service import build_memory_namespace

logger = logging.getLogger(__name__)


def search_memories(
    state: GraphState,
    runtime: Runtime[Context],
):
    user_id = runtime.context.user_id
    log_room_id = runtime.context.log_room_id
    log_room_member_id = runtime.context.log_room_member_id

    namespace = build_memory_namespace(user_id, log_room_id, log_room_member_id)
    kind_hint = state["retrieval_query"].kind_hint
    search_filter = None

    if kind_hint in ("semantic", "episodic"):
        search_filter = {"kind": kind_hint}

    results = runtime.store.search(
        namespace,
        query=state["retrieval_query"].retrieval_query,
        filter=search_filter,
        limit=10,
    )
    logger.debug("장기기억 검색 결과 | results=%s", results)

    final_results = [
        result for result in results if result.score is not None and result.score >= 0.5
    ]

    logger.info("search_memories 완료")
    logger.debug("장기기억 최종 검색 결과 | final_results=%s", final_results)

    return {
        "search_results": [
            SearchResult(
                content=result.value["content"],
                source_type=result.value["source_type"],
                occurred_at=result.value["occurred_at"],
            )
            for result in final_results
        ]
    }
