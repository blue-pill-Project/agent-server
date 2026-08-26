from agents.subgraphs.generate_log_image.llm import classify_image_category_llm
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategoryResult
from agents.subgraphs.generate_log_image.prompts import (
    build_visual_prompt_reference_search_query_instructions,
)
from agents.subgraphs.generate_log_image.llm import (
    build_visual_prompt_reference_search_query_llm,
)


def build_visual_prompt_reference_search_query(state: GraphState):
    hourly_plan_title = state["hourly_plan"].title
    hourly_plan_description = state["hourly_plan"].description
    hourly_plan_location = state["hourly_plan"].location
    hourly_plan_timeslot = state["hourly_plan"].timeslot

    formatted_prompt = build_visual_prompt_reference_search_query_instructions.format(
        hourly_plan_title=hourly_plan_title,
        hourly_plan_description=hourly_plan_description,
        hourly_plan_location=hourly_plan_location,
        hourly_plan_timeslot=hourly_plan_timeslot,
    )

    response = build_visual_prompt_reference_search_query_llm.invoke(formatted_prompt)

    return {"visual_prompt_reference_search_query": response.content}
