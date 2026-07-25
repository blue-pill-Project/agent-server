from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from ..subgraphs.image_to_prompt.graph import build_image_to_prompt_graph
from .state import GraphState
from .nodes import collect_images


image_to_prompt_graph = build_image_to_prompt_graph()
compiled_image_to_prompt_graph = image_to_prompt_graph.compile()


def call_image_to_prompt_graph(state):
    state = compiled_image_to_prompt_graph.invoke({"image_url": state["image_url"]})

    image_prompt = state["image_prompt"]

    visual_prompt_references = {
        "category": image_prompt.category.value,
        "participant_count": image_prompt.participant_count,
        "prompt": image_prompt.prompt,
        "embedding": state["embedding"],
    }

    return {"visual_prompt_references": [visual_prompt_references]}


def dispatch_image_to_prompt_graph(state: GraphState):
    target_urls = state["image_urls"][:]
    return [
        Send("call_image_to_prompt_graph", {"image_url": url}) for url in target_urls
    ]


def build_visual_prompt_reference_graph():
    graph = StateGraph(GraphState)

    graph.add_node("collect_images", collect_images)
    graph.add_node("call_image_to_prompt_graph", call_image_to_prompt_graph)

    graph.add_edge(START, "collect_images")
    graph.add_conditional_edges(
        "collect_images",
        dispatch_image_to_prompt_graph,
        ["call_image_to_prompt_graph"],
    )
    graph.add_edge("call_image_to_prompt_graph", END)

    return graph
