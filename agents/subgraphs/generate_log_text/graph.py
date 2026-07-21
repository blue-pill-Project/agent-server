from langgraph.graph import StateGraph, START, END
from agents.subgraphs.generate_log_text.nodes import generate_log_text
from agents.subgraphs.generate_log_text.state import GraphState


def build_generate_log_text_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("generate_log_text", generate_log_text)

    graph.add_edge(START, "generate_log_text")
    graph.add_edge("generate_log_text", END)

    return graph
