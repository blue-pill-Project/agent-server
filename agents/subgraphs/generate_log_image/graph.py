from langgraph.graph import StateGraph, START, END
from agents.subgraphs.generate_log_image.nodes import (
    build_visual_prompt_reference_search_query,
    classify_image_category,
    generate_image,
    build_final_image_prompt,
    retrieve_image_prompt,
)
from agents.subgraphs.generate_log_image.state import GraphState


def build_generate_log_image_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("retrieve_image_prompt", retrieve_image_prompt)
    # NOTE:
    # 1. build_visual_prompt_reference_search_query 해당 노드 쓸지 모르겠음
    # 2. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
    # graph.add_node("classify_image_category", classify_image_category)
    # graph.add_node(
    #     "build_visual_prompt_reference_search_query",
    #     build_visual_prompt_reference_search_query,
    # )
    graph.add_node("build_final_image_prompt", build_final_image_prompt)
    graph.add_node("generate_image", generate_image)

    graph.add_edge(START, "retrieve_image_prompt")
    # NOTE:
    # 1. build_visual_prompt_reference_search_query 해당 노드 쓸지 모르겠음
    # 2. classify_image_category는 우선 SOLO 사진 즉, 인물이 하나만 나오는 사진만 검색하기 위해 비활성화
    # graph.add_edge(START, "classify_image_category")
    # graph.add_edge(
    #     "build_visual_prompt_reference_search_query", "retrieve_image_prompt"
    # )
    graph.add_edge("retrieve_image_prompt", "build_final_image_prompt")
    graph.add_edge("build_final_image_prompt", "generate_image")
    graph.add_edge("generate_image", END)

    return graph
