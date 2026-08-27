from langgraph.runtime import Runtime

from agents.daily_logs_agent.state import Context
from agents.subgraphs.generate_log_image.state import GraphState
from agents.subgraphs.generate_log_image.prompts import (
    final_image_prompt_template,
    selfie_template,
    pov_template,
    third_person_template,
    replace_outfit_template,
    preserve_outfit_template,
)


def _build_outfit_instruction(outfit: str | None) -> str:
    """Hourly Plan의 의상 정보에 따라 의상 적용 지침을 생성한다."""

    if outfit and outfit.strip():
        return replace_outfit_template.format(outfit=outfit)
    else:
        return preserve_outfit_template


def _build_camera_style_instruction(camera_style: str) -> str:
    """촬영 방식에 따른 카메라 연출 지침을 생성한다."""

    if camera_style == "selfie":
        return selfie_template

    if camera_style == "pov":
        return pov_template

    return third_person_template


def build_final_image_prompt(
    state: GraphState,
    runtime: Runtime[Context],
) -> dict[str, str]:
    """현재 장면과 이미지 레퍼런스를 기반으로 최종 이미지 프롬프트를 생성한다."""

    hourly_plan = state["hourly_plan"]
    image_reference = state["image_reference"]

    outfit_instruction = _build_outfit_instruction(hourly_plan.outfit)

    camera_style_instruction = _build_camera_style_instruction(
        image_reference["camera_style"]
    )

    image_prompt = final_image_prompt_template.format(
        time_label=runtime.context.timeslot_label,
        visual_scene=state["visual_scene"],
        outfit_instruction=outfit_instruction,
        hourly_plan_location=hourly_plan.location,
        camera_style_instruction=camera_style_instruction,
    )

    return {
        "image_prompt": image_prompt,
    }
