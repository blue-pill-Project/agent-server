from agents.subgraphs.generate_hourly_plan.llm import generate_hourly_plan_llm
from agents.subgraphs.generate_hourly_plan.prompts import (
    generate_hourly_plan_instructions,
)
from agents.subgraphs.generate_hourly_plan.state import HourlyPlan, GraphState
from agents.daily_logs_agent.state import Context
from langgraph.runtime import Runtime
import logging

logger = logging.getLogger(__name__)


def generate_hourly_plan(
    state: GraphState,
    runtime: Runtime[Context],
) -> dict:
    log_room_member_prompt = runtime.context.log_room_member_prompt
    today_plan = runtime.context.today_plan
    timeslot = runtime.context.timeslot
    previous_plans = runtime.context.previous_plans
    memories = state["long_term_memories"]

    memory_context = "\n".join(f"- {memory}" for memory in memories if memories)

    logger.debug("used today plan | today_plan=%s", today_plan)
    logger.debug(
        "used long term memories | count=%d\n%s",
        len(memories),
        "\n".join(f"- {memory}" for memory in memories),
    )
    logger.debug(
        "used previous plans | count=%d\n%s",
        len(previous_plans),
        "\n".join(f"- {plan}" for plan in previous_plans),
    )

    formatted_prompt = generate_hourly_plan_instructions.format(
        log_room_member_prompt=log_room_member_prompt,
        today_plan=today_plan,
        previous_plans=previous_plans,
        timeslot=timeslot,
        memory_context=memory_context,
    )
    logger.info("generate_hourly_plan 완료")

    structured_model = generate_hourly_plan_llm.with_structured_output(HourlyPlan)
    response = structured_model.invoke(formatted_prompt)
    return {"hourly_plan": response}
