from agents.subgraphs.generate_log_image.llm import classify_image_category_llm
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategoryResult
from agents.subgraphs.generate_log_image.prompts import (
    build_visual_prompt_reference_search_query_instructions,
)


def build_visual_prompt_reference_search_query(state: GraphState):
    hourly_plan_description = state["hourly_plan"].description
    formatted_prompt = build_visual_prompt_reference_search_query_instructions.format(
        hourly_plan_description=hourly_plan_description
    )

    response = classify_image_category_llm.invoke(formatted_prompt)

    return {"visual_prompt_reference_search_query": response.content}
