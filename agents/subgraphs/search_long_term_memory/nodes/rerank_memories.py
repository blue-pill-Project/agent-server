from agents.subgraphs.search_long_term_memory.state import GraphState, Context
from langgraph.runtime import Runtime
from common.utils.reranker import BgeReranker


def rerank_memories(
    state: GraphState,
    runtime: Runtime[Context],
):

    # TODO: agent에서 주입으로 빼야할듯
    reranker = BgeReranker()

    results = reranker.rerank(
        query=state["retrieval_query"].retrieval_query,
        documents=[result.content for result in state["search_results"]],
        top_k=3,
    )

    final_long_term_memories = [result.content for result in results]
    print(f"💙 검색된 장기기억: {final_long_term_memories}")
    return {
        "reranked_results": results,
        "final_long_term_memories": final_long_term_memories,
    }
