from agents.subgraphs.generate_log_image.llm import build_final_image_prompt_llm
from agents.subgraphs.generate_log_image.state import GraphState
from agents.subgraphs.generate_log_image.prompts import (
    build_final_image_prompt_instructions,
)


def build_final_image_prompt(state: GraphState):
    hourly_plan_timeslot = state["hourly_plan"].timeslot
    hourly_plan_description = state["hourly_plan"].description
    hourly_plan_outfit = state["hourly_plan"].outfit
    hourly_plan_location = state["hourly_plan"].location

    formatted_prompt = build_final_image_prompt_instructions.format(
        hourly_plan_timeslot=hourly_plan_timeslot,
        hourly_plan_description=hourly_plan_description,
        hourly_plan_outfit=hourly_plan_outfit,
        hourly_plan_location=hourly_plan_location,
    )
    response = build_final_image_prompt_llm.invoke(formatted_prompt)

    return {"image_prompt": response.content}
