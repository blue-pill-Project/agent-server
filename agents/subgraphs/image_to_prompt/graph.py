from langgraph.graph import StateGraph, START, END

from agents.subgraphs.image_to_prompt.state import GraphState
from agents.subgraphs.image_to_prompt.nodes import (
    convert_img_to_base64,
    extract_prompt_from_image,
    embed_image_prompt,
)


def build_image_to_prompt_graph():
    graph = StateGraph(GraphState)

    graph.add_node("convert_img_to_base64", convert_img_to_base64)
    graph.add_node("extract_prompt_from_image", extract_prompt_from_image)
    graph.add_node("embed_image_prompt", embed_image_prompt)

    graph.add_edge(START, "convert_img_to_base64")
    graph.add_edge("convert_img_to_base64", "extract_prompt_from_image")
    graph.add_edge("extract_prompt_from_image", "embed_image_prompt")
    graph.add_edge("embed_image_prompt", END)

    return graph
