from agents.weekly_plan_agent.llm import generate_weekly_plan_llm
from agents.weekly_plan_agent.state import Context, WeeklyPlan, GraphState
from agents.weekly_plan_agent.prompts import generate_weekly_plan_instructions
from langgraph.runtime import Runtime


def generate_weekly_plan(state: GraphState, runtime: Runtime[Context]) -> str:
    week_dates = runtime.context.week_dates
    log_room_member_prompt = runtime.context.log_room_member_prompt

    selected_trends = state["selected_trends"]

    formatted_prompt = generate_weekly_plan_instructions.format(
        week_dates=week_dates,
        log_room_member_prompt=log_room_member_prompt,
        selected_trends=selected_trends,
    )
    structured_model = generate_weekly_plan_llm.with_structured_output(WeeklyPlan)
    response = structured_model.invoke(formatted_prompt)
    return {"weekly_plan": response}
