from agents.subgraphs.generate_log_image.llm import classify_image_category_llm
from agents.subgraphs.generate_log_image.state import GraphState, ImageCategoryResult
from agents.subgraphs.generate_log_image.prompts import (
    build_visual_scene_instructions,
)
from agents.subgraphs.generate_log_image.llm import (
    build_visual_scene_llm,
)
import logging

logger = logging.getLogger(__name__)


def build_visual_scene(state: GraphState):
    hourly_plan_title = state["hourly_plan"].title
    hourly_plan_description = state["hourly_plan"].description
    hourly_plan_location = state["hourly_plan"].location
    hourly_plan_timeslot = state["hourly_plan"].timeslot

    formatted_prompt = build_visual_scene_instructions.format(
        hourly_plan_title=hourly_plan_title,
        hourly_plan_description=hourly_plan_description,
        hourly_plan_location=hourly_plan_location,
        hourly_plan_timeslot=hourly_plan_timeslot,
    )

    response = build_visual_scene_llm.invoke(formatted_prompt)
    logger.debug(
        "hourly plan description | hourly_plan_description=%s", hourly_plan_description
    )
    logger.info("build_visual_scene 완료")
    return {"visual_scene": response.content}
