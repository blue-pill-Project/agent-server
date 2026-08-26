from agents.subgraphs.generate_log_image.llm import build_final_image_prompt_llm
from agents.subgraphs.generate_log_image.state import GraphState
from agents.subgraphs.generate_log_image.prompts import final_image_prompt_template
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context


# TODO:  수정해야함 전체적인 구조 수정
def build_final_image_prompt(state: GraphState, runtime: Runtime[Context]):
    timeslot_label = runtime.context.timeslot_label
    visual_scene = state["visual_scene"]
    hourly_plan_outfit = state["hourly_plan"].outfit
    hourly_plan_location = state["hourly_plan"].location

    outfit_instruction = (
        f"첫 번째 캐릭터 레퍼런스의 기존 의상은 사용하지 않고 "
        f"{hourly_plan_outfit}을 착용시킨다."
        if hourly_plan_outfit and hourly_plan_outfit.strip()
        else (
            "첫 번째 캐릭터 레퍼런스에 나타난 의복 착용 상태와 "
            "신체 노출 범위를 그대로 유지하며, 의상을 새로 추가하거나 제거하지 않는다. "
            "노출된 신체는 비성적이고 자연스럽게 표현한다."
        )
    )

    formatted_template = final_image_prompt_template.format(
        time_label=timeslot_label,
        visual_scene=visual_scene,
        outfit_instruction=outfit_instruction,
        hourly_plan_location=hourly_plan_location,
    )

    return {"image_prompt": formatted_template}
