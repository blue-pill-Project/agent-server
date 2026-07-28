from langgraph.graph import StateGraph, START, END
from agents.visual_prompt_reference.state import (
    Context,
    GraphState,
    VisualPromptReference,
)
from agents.visual_prompt_reference.nodes import (
    extract_prompt_from_image,
    extract_situation_from_image,
)
from langgraph.runtime import Runtime


def aggregate_visual_prompt_reference_outputs(
    state: GraphState, runtime: Runtime[Context]
):
    shot_spec = state["shot_spec"]
    situation = state["situation"]

    visual_prompt_reference = VisualPromptReference(
        category=shot_spec.category,
        participant_count=shot_spec.participant_count,
        prompt=shot_spec.prompt,
        situation=situation,
    )

    return {
        "visual_prompt_reference": visual_prompt_reference,
    }


def build_visual_prompt_reference_graph():
    graph = StateGraph(GraphState)

    graph.add_node("extract_prompt_from_image", extract_prompt_from_image)
    graph.add_node("extract_situation_from_image", extract_situation_from_image)
    graph.add_node(
        "aggregate_visual_prompt_reference_outputs",
        aggregate_visual_prompt_reference_outputs,
    )

    graph.add_edge(START, "extract_prompt_from_image")
    graph.add_edge(START, "extract_situation_from_image")
    graph.add_edge(
        "extract_prompt_from_image", "aggregate_visual_prompt_reference_outputs"
    )
    graph.add_edge(
        "extract_situation_from_image", "aggregate_visual_prompt_reference_outputs"
    )
    graph.add_edge("aggregate_visual_prompt_reference_outputs", END)

    return graph
