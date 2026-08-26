from langgraph.graph import StateGraph, START, END
from agents.subgraphs.generate_log_image.nodes import (
    build_visual_scene,
    # classify_image_category,
    generate_image,
    build_final_image_prompt,
    rerank_visual_prompt_references,
    retrieve_visual_prompt_references,
)
from agents.subgraphs.generate_log_image.state import GraphState


# NOTE:
# 1. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
# graph.add_node("classify_image_category", classify_image_category)
def build_generate_log_image_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node(
        "retrieve_visual_prompt_references", retrieve_visual_prompt_references
    )
    graph.add_node(
        "build_visual_scene",
        build_visual_scene,
    )
    graph.add_node("rerank_visual_prompt_references", rerank_visual_prompt_references)
    graph.add_node("build_final_image_prompt", build_final_image_prompt)
    graph.add_node("generate_image", generate_image)

    graph.add_edge(START, "build_visual_scene")
    graph.add_edge(
        "build_visual_scene",
        "retrieve_visual_prompt_references",
    )
    graph.add_edge(
        "retrieve_visual_prompt_references", "rerank_visual_prompt_references"
    )
    graph.add_edge("rerank_visual_prompt_references", "build_final_image_prompt")
    graph.add_edge("build_final_image_prompt", "generate_image")
    graph.add_edge("generate_image", END)

    return graph
