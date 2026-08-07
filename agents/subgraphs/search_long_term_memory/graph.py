from langgraph.graph import StateGraph, START, END

from agents.subgraphs.search_long_term_memory.nodes import (
    build_retrieval_query,
    rerank_memories,
    search_memories,
)
from agents.subgraphs.search_long_term_memory.state import GraphState


def route_after_build_retrieval_query(
    state: GraphState,
) -> str:
    if not state["retrieval_query"].should_search:
        return "done"

    return "search"


def build_search_long_term_memory_graph():
    graph = StateGraph(GraphState)

    graph.add_node("build_retrieval_query", build_retrieval_query)
    graph.add_node("search_memories", search_memories)
    graph.add_node("rerank_memories", rerank_memories)
    
    graph.add_edge(START, "build_retrieval_query")

    graph.add_conditional_edges(
        "build_retrieval_query",
        route_after_build_retrieval_query,
        {
            "search": ("search_memories"),
            "done": END,
        },
    )
    graph.add_edge("search_memories", "rerank_memories")
    graph.add_edge("rerank_memories", END)

    return graph
