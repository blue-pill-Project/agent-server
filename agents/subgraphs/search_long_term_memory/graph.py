from langgraph.graph import StateGraph, START, END

from agents.subgraphs.search_long_term_memory.nodes import (
    build_chat_retrieval_query,
    build_post_retrieval_query,
    rerank_memories,
    search_memories,
)
from agents.subgraphs.search_long_term_memory.state import GraphState


def route_purpose(
    state: GraphState,
) -> str:
    return state["source"].purpose


def route_after_build_retrieval_query(
    state: GraphState,
) -> str:
    if not state["retrieval_query"].should_search:
        return "done"

    return "search"


# TODO: 이거 롱텀메모리 키에러 안나게 빈값처리 다른 방법 생각해보기
def set_empty_long_term_memories(
    state: GraphState,
) -> dict:
    return {
        "final_long_term_memories": [],
    }


def build_search_long_term_memory_graph():
    graph = StateGraph(GraphState)

    graph.add_node("build_post_retrieval_query", build_post_retrieval_query)
    graph.add_node("build_chat_retrieval_query", build_chat_retrieval_query)
    graph.add_node("set_empty_long_term_memories", set_empty_long_term_memories)
    graph.add_node("search_memories", search_memories)
    graph.add_node("rerank_memories", rerank_memories)

    graph.add_conditional_edges(
        START,
        route_purpose,
        {
            "post": ("build_post_retrieval_query"),
            "chat": ("build_chat_retrieval_query"),
        },
    )

    graph.add_conditional_edges(
        "build_post_retrieval_query",
        route_after_build_retrieval_query,
        {
            "search": ("search_memories"),
            "done": "set_empty_long_term_memories",
        },
    )

    graph.add_conditional_edges(
        "build_chat_retrieval_query",
        route_after_build_retrieval_query,
        {
            "search": ("search_memories"),
            "done": "set_empty_long_term_memories",
        },
    )

    graph.add_edge("search_memories", "rerank_memories")
    graph.add_edge("rerank_memories", END)
    graph.add_edge("set_empty_long_term_memories", END)

    return graph
