from langgraph.graph import StateGraph, START, END
from agents.chat_rule_agent.nodes import generate_chat_rule
from agents.chat_rule_agent.state import GraphState


def build_generate_chat_rule_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("generate_chat_rule", generate_chat_rule)

    graph.add_edge(START, "generate_chat_rule")
    graph.add_edge("generate_chat_rule", END)

    return graph
