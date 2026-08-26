from agents.subgraphs.generate_log_image.llm import build_final_image_prompt_llm
from agents.subgraphs.generate_log_image.state import GraphState
from agents.subgraphs.generate_log_image.prompts import final_image_prompt_template
from langgraph.runtime import Runtime
from agents.daily_logs_agent.state import Context


# TODO:  수정해야함 전체적인 구조 수정
def build_final_image_prompt(state: GraphState, runtime: Runtime[Context]):
    timeslot_label = runtime.context.timeslot_label
    hourly_plan_description = state["hourly_plan"].description
    hourly_plan_outfit = state["hourly_plan"].outfit
    hourly_plan_location = state["hourly_plan"].location

    outfit_instruction = (
        f"캐릭터의 기존 의상은 사용하지 않고 {hourly_plan_outfit}을 착용시킨다."
        if hourly_plan_outfit
        else "장소와 상황에 어울리는 단순하고 비성적인 기본 복장을 입힌다."
    )

    formatted_template = final_image_prompt_template.format(
        time_label=timeslot_label,
        hourly_plan_description=hourly_plan_description,
        outfit_instruction=outfit_instruction,
        hourly_plan_location=hourly_plan_location,
    )

    return {"image_prompt": formatted_template}
