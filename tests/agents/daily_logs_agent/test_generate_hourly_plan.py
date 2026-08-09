from collections.abc import Callable
from typing import Any
from uuid import uuid4

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.daily_logs_agent.graph import build_daily_logs_graph
from agents.daily_logs_agent.state import Context

from tests.agents.daily_logs_agent.cases import DAILY_LOG_CASES, DailyLogCase


def create_config(case_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": f"daily-logs-{case_id}-{uuid4()}",
        }
    }


@pytest.mark.parametrize(
    "case",
    DAILY_LOG_CASES,
    ids=lambda case: case.id,
)
@pytest.mark.asyncio
async def test_generate_hourly_plan_for_multiple_daily_scenarios(
    case: DailyLogCase,
    context_factory: Callable[[DailyLogCase], Context],
    memory_store: AsyncPostgresStore,
    hourly_plan_report: list[dict[str, Any]],
) -> None:
    graph = build_daily_logs_graph().compile(
        checkpointer=InMemorySaver(),
        store=memory_store,
    )
    context = context_factory(case)

    result = await graph.ainvoke(
        {},
        config=create_config(case.id),
        context=context,
        interrupt_after=["call_generate_hourly_plan_graph"],
    )

    hourly_plan = result.get("hourly_plan")

    assert hourly_plan is not None

    # assertion 전에 수집하면 뒤쪽 assertion이 실패해도 생성 결과를 볼 수 있음
    hourly_plan_report.append(
        {
            "case_id": case.id,
            "timeslot": case.timeslot,
            "today_plan": case.today_plan,
            "previous_plans": list(case.previous_plans),
            "hourly_plan": hourly_plan.model_dump(mode="json"),
        }
    )

    assert hourly_plan.timeslot == case.timeslot
    assert hourly_plan.title
    assert hourly_plan.description
    assert hourly_plan.outfit
    assert hourly_plan.location
