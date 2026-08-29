from agents.subgraphs.search_long_term_memory.state import GraphState, Context
from langgraph.runtime import Runtime
import logging

logger = logging.getLogger(__name__)


def rerank_memories(
    state: GraphState,
    runtime: Runtime[Context],
):
    reranker = runtime.context.reranker

    results = reranker.rerank(
        query=state["retrieval_query"].retrieval_query,
        documents=[result.content for result in state["search_results"]],
        top_k=3,
    )

    final_long_term_memories = [result.content for result in results]
    logger.info("rerank_memories 완료")
    logger.debug(
        "rerank memories | top_1=%s | top_2=%s | top_3=%s ",
        final_long_term_memories[0],
        final_long_term_memories[1],
        final_long_term_memories[2],
    )
    return {
        "reranked_results": results,
        "final_long_term_memories": final_long_term_memories,
    }
