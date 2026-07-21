from agents.subgraphs.generate_hourly_plan.llm import generate_hourly_plan_llm
from agents.subgraphs.generate_hourly_plan.prompts import (
    generate_hourly_plan_instructions,
)
from agents.subgraphs.generate_hourly_plan.state import HourlyPlan, GraphState
from agents.daily_logs_agent.state import Context
from langgraph.runtime import Runtime


def generate_hourly_plan(
    state: GraphState,
    runtime: Runtime[Context],
) -> dict:
    log_room_member_prompt = runtime.context.log_room_member_prompt
    today_plan = runtime.context.today_plan
    timeslot = runtime.context.timeslot
    previous_plans = runtime.context.previous_plans
    memories = state["long_term_memories"]

    memory_context = "\n".join(
        f"- {memory.get('data')}" for memory in memories if memory.get("data")
    )

    formatted_prompt = generate_hourly_plan_instructions.format(
        log_room_member_prompt=log_room_member_prompt,
        today_plan=today_plan,
        previous_plans=previous_plans,
        timeslot=timeslot,
        memory_context=memory_context,
    )

    structured_model = generate_hourly_plan_llm.with_structured_output(HourlyPlan)
    response = structured_model.invoke(formatted_prompt)
    return {"hourly_plan": response}
