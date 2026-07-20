from langgraph.runtime import Runtime
from agents.weekly_plan_agent.llm import select_trends_llm
from agents.weekly_plan_agent.state import Context, SelectedTrends, GraphState
from agents.weekly_plan_agent.prompts import select_trends_instructions


def select_trends(state: GraphState, runtime: Runtime[Context]) -> str:
    current_month = runtime.context.current_month
    log_room_member_prompt = runtime.context.log_room_member_prompt
    trends = runtime.context.trends

    formatted_prompt = select_trends_instructions.format(
        current_month=current_month,
        log_room_member_prompt=log_room_member_prompt,
        trends=trends,
    )
    structured_model = select_trends_llm.with_structured_output(
        SelectedTrends, method="json_schema"
    )
    response = structured_model.invoke(formatted_prompt)
    return {"selected_trends": response}
