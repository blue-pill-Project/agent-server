from langgraph.graph import StateGraph, START, END
from agents.character_chat_agent.nodes import (
    generate_reply,
    decide_memory_storage,
    store_long_term_memory,
)
from agents.character_chat_agent.state import GraphState, Context


def route_memory_storage(state):
    if state["memory_decision"].should_save:
        return "store_long_term_memory"

    return "__end__"


def build_character_chat_graph():
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("generate_reply", generate_reply)
    graph.add_node("decide_memory_storage", decide_memory_storage)
    graph.add_node("store_long_term_memory", store_long_term_memory)

    graph.add_edge(START, "decide_memory_storage")
    graph.add_edge(START, "generate_reply")
    graph.add_edge("generate_reply", END)
    graph.add_conditional_edges(
        "decide_memory_storage",
        route_memory_storage,
        {
            "store_long_term_memory": "store_long_term_memory",
            "__end__": END,
        },
    )
    graph.add_edge("store_long_term_memory", END)

    return graph
