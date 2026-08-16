from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from agents.subgraphs.write_long_term_memory.nodes import (
    extract_memory_candidates,
    write_memory,
)
from agents.subgraphs.write_long_term_memory.state import GraphState


def route_after_extraction(
    state: GraphState,
) -> str:
    if not state["memories"]:
        return "done"

    return "write"


def build_write_long_term_memory_graph():
    graph = StateGraph(GraphState)

    graph.add_node("extract_memory_candidates", extract_memory_candidates)
    graph.add_node("write_memory", write_memory)

    graph.add_edge(START, "extract_memory_candidates")

    graph.add_conditional_edges(
        "extract_memory_candidates",
        route_after_extraction,
        {
            "write": ("write_memory"),
            "done": END,
        },
    )

    graph.add_edge("write_memory", END)

    return graph
