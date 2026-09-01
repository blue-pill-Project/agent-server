from langgraph.graph import StateGraph, START, END
from agents.subgraphs.generate_log_image.nodes import (
    build_visual_scene,
    # classify_image_category,
    generate_image,
    build_final_image_prompt,
    rerank_visual_prompt_references,
    retrieve_visual_prompt_references,
    get_default_selfie_visual_prompt_reference,
)
from agents.subgraphs.generate_log_image.state import GraphState


def route_after_retrieve(
    state: GraphState,
) -> str:
    if state["use_default_reference"]:
        return "default"

    if not state["image_references"]:
        return "final"

    return "rerank"


# NOTE:
# 1. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
# graph.add_node("classify_image_category", classify_image_category)
def build_generate_log_image_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    ##========NODE========##
    graph.add_node(
        "retrieve_visual_prompt_references", retrieve_visual_prompt_references
    )
    graph.add_node(
        "build_visual_scene",
        build_visual_scene,
    )
    graph.add_node("rerank_visual_prompt_references", rerank_visual_prompt_references)
    graph.add_node(
        "get_default_selfie_visual_prompt_reference",
        get_default_selfie_visual_prompt_reference,
    )
    graph.add_node("build_final_image_prompt", build_final_image_prompt)
    graph.add_node("generate_image", generate_image)

    ##========EDGE========##
    graph.add_edge(START, "build_visual_scene")
    graph.add_edge(
        "build_visual_scene",
        "retrieve_visual_prompt_references",
    )
    graph.add_conditional_edges(
        "retrieve_visual_prompt_references",
        route_after_retrieve,
        {
            "default": "get_default_selfie_visual_prompt_reference",
            "rerank": "rerank_visual_prompt_references",
            "final": "build_final_image_prompt",
        },
    )
    graph.add_edge(
        "get_default_selfie_visual_prompt_reference", "build_final_image_prompt"
    )
    graph.add_edge("rerank_visual_prompt_references", "build_final_image_prompt")
    graph.add_edge("build_final_image_prompt", "generate_image")
    graph.add_edge("generate_image", END)

    return graph
