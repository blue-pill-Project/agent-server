from langgraph.graph import StateGraph, START, END
from agents.character_chat_agent.nodes import (
    classify_intent,
    generate_reply,
    answer_with_search,
    decide_memory_storage,
    store_long_term_memory,
)
from agents.character_chat_agent.state import GraphState, Context

def route_intent(state):
    return state["intent_decision"].intent

def route_memory_storage(state):
    if state["memory_decision"].should_save:
        return "store_long_term_memory"

    return "__end__"


def build_character_chat_graph():
    graph = StateGraph(
        GraphState,
        context_schema=Context,
    )

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("answer_with_search", answer_with_search)
    graph.add_node("answer_fallback", generate_reply)
    graph.add_node("decide_memory_storage", decide_memory_storage)
    graph.add_node("store_long_term_memory", store_long_term_memory)

    graph.add_edge(START, "classify_intent")
    graph.add_edge(START, "decide_memory_storage")

    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "search": "answer_with_search",
            "other": "answer_fallback",
        },
    )

    graph.add_edge("answer_with_search", END)
    graph.add_edge("answer_fallback", END)

    graph.add_conditional_edges(
        "decide_memory_storage",
        route_memory_storage,
        {"store_long_term_memory": "store_long_term_memory", "__end__": END},
    )
    graph.add_edge("store_long_term_memory", END)

    return graph
