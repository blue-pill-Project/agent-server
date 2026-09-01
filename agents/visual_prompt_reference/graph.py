from langgraph.graph import StateGraph, START, END
from agents.visual_prompt_reference.state import GraphState
from agents.visual_prompt_reference.nodes import extract_info_from_image


def build_visual_prompt_reference_graph():
    graph = StateGraph(GraphState)

    graph.add_node("extract_info_from_image", extract_info_from_image)

    graph.add_edge(START, "extract_info_from_image")
    graph.add_edge("extract_info_from_image", END)

    return graph
